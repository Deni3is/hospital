from io import BytesIO

import xlwt
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .forms import DeviceForm, PatientForm
from .models import Device, Patient


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class DashboardView(TemplateView):
    template_name = "registry/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_tab = self.request.GET.get("tab", "patients")
        if active_tab not in {"patients", "devices"}:
            active_tab = "patients"

        context.update(
            active_tab=active_tab,
            patients=Patient.objects.order_by("id"),
            devices=Device.objects.order_by("id"),
        )
        return context


class ExportTableView(View):
    patient_headers = ["ID", "Пол", "Дата рождения", "Возраст"]
    device_headers = ["ID", "UID1", "UID2", "UID3", "Марка", "Модель", "Название"]

    def get(self, request, target, file_format, *args, **kwargs):
        if target == "patients":
            headers = self.patient_headers
            rows = [
                [patient.id, patient.get_gender_display(), patient.birth_date.strftime("%d.%m.%Y"), patient.age]
                for patient in Patient.objects.order_by("id")
            ]
            filename = f"patients.{file_format}"
        elif target == "devices":
            headers = self.device_headers
            rows = [
                [
                    device.id,
                    device.uid1,
                    device.uid2,
                    device.uid3,
                    device.get_brand_display(),
                    device.model,
                    device.name,
                ]
                for device in Device.objects.order_by("id")
            ]
            filename = f"devices.{file_format}"
        else:
            raise Http404("Неизвестный тип таблицы.")

        if file_format == "xls":
            return self._build_xls_response(headers, rows, filename)
        if file_format == "pdf":
            return self._build_pdf_response(headers, rows, filename)
        raise Http404("Неизвестный формат выгрузки.")

    def _build_xls_response(self, headers, rows, filename):
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Export")
        header_style = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour ice_blue;")

        for column_index, header in enumerate(headers):
            sheet.write(0, column_index, header, header_style)
            sheet.col(column_index).width = 5000

        for row_index, row in enumerate(rows, start=1):
            for column_index, value in enumerate(row):
                sheet.write(row_index, column_index, value)

        buffer = BytesIO()
        workbook.save(buffer)
        response = HttpResponse(buffer.getvalue(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    def _build_pdf_response(self, headers, rows, filename):
        buffer = BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            leftMargin=24,
            rightMargin=24,
            topMargin=24,
            bottomMargin=24,
        )
        table_data = [headers, *rows] if rows else [headers, ["Нет данных для выгрузки"] + [""] * (len(headers) - 1)]
        table = Table(table_data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfe7ef")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
                    ("PADDING", (0, 0), (-1, -1), 6),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        document.build([table])
        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "registry/patient_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            form_title="Добавить пациента",
            form_submit_label="Сохранить",
            cancel_url=reverse("dashboard") + "?tab=patients",
        )
        return context

    def get_success_url(self):
        return reverse("dashboard") + "?tab=patients"


class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "registry/patient_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            form_title="Изменить пациента",
            form_submit_label="Обновить",
            cancel_url=reverse("dashboard") + "?tab=patients",
        )
        return context

    def get_success_url(self):
        return reverse("dashboard") + "?tab=patients"


class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = "registry/device_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            form_title="Добавить устройство",
            form_submit_label="Сохранить",
            cancel_url=reverse("dashboard") + "?tab=devices",
        )
        return context

    def get_success_url(self):
        return reverse("dashboard") + "?tab=devices"


class DeviceUpdateView(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = "registry/device_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            form_title="Изменить устройство",
            form_submit_label="Обновить",
            cancel_url=reverse("dashboard") + "?tab=devices",
        )
        return context

    def get_success_url(self):
        return reverse("dashboard") + "?tab=devices"


class DeviceDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        device = get_object_or_404(Device, pk=pk)
        device.delete()
        return redirect(reverse("dashboard") + "?tab=devices")
