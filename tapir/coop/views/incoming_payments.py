import django_filters
import django_tables2
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.html import format_html
from django.views import generic
from django_filters.views import FilterView
from django_tables2 import SingleTableView

from tapir.coop.forms import IncomingPaymentForm
from tapir.coop.models import IncomingPayment
from tapir.utils.forms import DateInput


class IncomingPaymentTable(django_tables2.Table):
    class Meta:
        model = IncomingPayment
        template_name = "django_tables2/bootstrap4.html"
        fields = [
            "paying_member",
            "credited_member",
            "amount",
            "payment_date",
            "creation_date",
            "comment",
            "created_by",
        ]
        order_by = "payment_date"

    def render_paying_member(self, value, record: IncomingPayment):
        return format_html(
            "<a href={}>{}</a>",
            record.paying_member.get_absolute_url(),
            record.paying_member.get_info().get_display_name(),
        )

    def render_credited_member(self, value, record: IncomingPayment):
        return format_html(
            "<a href={}>{}</a>",
            record.credited_member.get_absolute_url(),
            record.credited_member.get_info().get_display_name(),
        )

    def render_created_by(self, value, record: IncomingPayment):
        return format_html(
            "<a href={}>{}</a>",
            record.created_by.get_absolute_url(),
            record.created_by.get_display_name(),
        )

    def render_payment_date(self, value, record: IncomingPayment):
        return record.payment_date.strftime("%d.%m.%Y")

    def render_creation_date(self, value, record: IncomingPayment):
        return record.payment_date.strftime("%d.%m.%Y")


class IncomingPaymentFilter(django_filters.FilterSet):
    class Meta:
        model = IncomingPayment
        fields = [
            "paying_member",
            "credited_member",
            "created_by",
            "payment_date",  # TODO Théo 04.06.22 : use from/to date instead of an exact one
            "creation_date",
        ]
        widgets = {
            "payment_date": DateInput()
        }  # TODO Théo 06.06.22 : find out how to set widgets in filter forms


class IncomingPaymentListView(PermissionRequiredMixin, FilterView, SingleTableView):
    table_class = IncomingPaymentTable
    model = IncomingPayment
    template_name = "coop/incoming_payment_list.html"
    permission_required = "coop.manage"

    filterset_class = IncomingPaymentFilter


class IncomingPaymentCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = "coop.manage"
    model = IncomingPayment
    form_class = IncomingPaymentForm

    def get_success_url(self):
        return reverse("coop:incoming_payment_list")
