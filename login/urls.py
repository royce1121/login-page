from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(
        r'^$',
        views.StartPageView.as_view(),
        name='start_page'
    ),
	url(
		r'^accounts/details/$',
		views.LandingPageView.as_view(),
		name='landing_page',
	),
	url(
		r'^creation/steps/first/$',
		views.StepPageView.as_view(),
		name='steps',
	),
	url(
		r'^creation/steps/second/$',
		views.SecondStepPageView.as_view(),
		name='steps_2',
	),
	url(
		r'^creation/steps/third/$',
		views.ThirdStepPageView.as_view(),
		name='steps_3',
	),
	url(
		r'^accounts/~ajax/$',
		views.AccountDataAjax.as_view(),
		name='account_ajax'
	),
]