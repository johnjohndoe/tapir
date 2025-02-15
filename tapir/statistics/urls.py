from django.urls import path

from tapir.statistics import views

app_name = "statistics"
urlpatterns = [
    path(
        "main_statistics",
        views.MainStatisticsView.as_view(),
        name="main_statistics",
    ),
    path(
        "member_count_evolution_json",
        views.MemberCountEvolutionJsonView.as_view(),
        name="member_count_evolution_json",
    ),
    path(
        "new_members_per_month_json",
        views.NewMembersPerMonthJsonView.as_view(),
        name="new_members_per_month_json",
    ),
    path(
        "purchasing_members_json",
        views.PurchasingMembersJsonView.as_view(),
        name="purchasing_members_json",
    ),
    path(
        "working_members_json",
        views.WorkingMembersJsonView.as_view(),
        name="working_members_json",
    ),
    path(
        "frozen_members_json",
        views.FrozenMembersJsonView.as_view(),
        name="frozen_members_json",
    ),
    path(
        "co_purchasers_json",
        views.CoPurchasersJsonView.as_view(),
        name="co_purchasers_json",
    ),
    path(
        "financing_campaign_json/<int:pk>",
        views.FinancingCampaignJsonView.as_view(),
        name="financing_campaign_json",
    ),
]
