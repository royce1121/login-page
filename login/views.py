from .forms import BaseAccountForm
from .forms import FirstStepForm
from .forms import SecondStepForm
from .forms import ThirdStepForm
from .forms import UserForm
from .models import BaseAccountModel
from braces.views import AjaxResponseMixin
from braces.views import JsonRequestResponseMixin
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ViewsDispatcher(View):
	def dispatch(self, request, *args, **kwargs):
		user = self.request.user

		basic_info = BaseAccountModel.objects.filter(
			user=user
		).first()
		if basic_info:
			if not basic_info.is_data_complete():
				if basic_info.is_step_two_complete():
					return redirect(reverse(
						'steps_3',
					))
				if basic_info.is_step_one_complete():
					return redirect(reverse(
						'steps_2',
					))
		else:
			return redirect(reverse(
				'steps',
			))

		return super().dispatch(request, *args, **kwargs)


class StartPageView(FormView):
	template_name = "index.html"
	form_class  = UserForm

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect(reverse(
				'landing_page',
			))

		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(
		    StartPageView, self
		).get_context_data(**kwargs)

		form = UserForm()

		context.update({
			'login_type': 'Login',
		    'form': form,
		})
		return context

	def post(self, request, *args, **kwargs):

		username = self.request.POST.get('username')
		password = self.request.POST.get('password')
		login_type = self.request.POST.get('login_type')
		form = UserForm(
			data=self.request.POST,
		)
		if login_type == 'Register':
			if form.is_valid():
				user = User.objects.create_user(username,None,password)
				login(request, user)
			else:
				return render(
					request,
					'index.html',
					{
						'form': form,
						'login_type': 'Register'
					}
				)
		else:
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
			else:
				messages.error(self.request, _('User not existing in the database.'))
				return render(
					request,
					'index.html',
					{
						'form': form,
						'login_type': 'Login'
					}
				)

		return redirect(reverse(
            'landing_page',
        ))


class LandingPageView(
	LoginRequiredMixin,
	FormView,
	ViewsDispatcher,
):
	template_name = "landing_page.html"
	login_url = 'start_page'
	form_class = BaseAccountForm

	def get_object(self):
		basic_account = BaseAccountModel.objects.filter(user=self.request.user).first()

		return basic_account

	def get_form_kwargs(self, **kwargs):
		extra_kwargs = super(LandingPageView, self).get_form_kwargs(**kwargs)
		extra_kwargs.update({
		    'user': self.request.user,
		    'instance': self.get_object(),
		})
		return extra_kwargs

	def get_context_data(self, **kwargs):
		context = super(
		    LandingPageView, self
		).get_context_data(**kwargs)

		context.update({
			'object': self.get_object(),
		})
		return context

	def post(self, request, *args, **kwargs):
		logout(request)
		return redirect(reverse(
            'start_page',
        ))


class StepPageView(
	LoginRequiredMixin,
	FormView,
):
	template_name = "steps.html"
	form_class  = FirstStepForm
	prev_page = None
	next_page = 'steps_2'

	def dispatch(self, request, *args, **kwargs):
		user = self.request.user

		basic_info = BaseAccountModel.objects.filter(
			user=user
		).first()
		if basic_info:
			if basic_info.is_data_complete():
				return redirect(reverse(
					'landing_page',
				))

		return super().dispatch(request, *args, **kwargs)

	def get_object(self):
		basic_account = BaseAccountModel.objects.filter(user=self.request.user)
		if basic_account:
		    return basic_account.first()
		else:
		    return None

	def get_form_kwargs(self, **kwargs):
		extra_kwargs = super(StepPageView, self).get_form_kwargs(**kwargs)
		extra_kwargs.update({
		    'user': self.request.user,
		    'instance': self.get_object(),
		})
		return extra_kwargs

	def get_context_data(self, **kwargs):
		context = super(
		    StepPageView, self
		).get_context_data(**kwargs)

		steps = [
			{
			    'active': True,
			    'url': reverse('steps'),
			    'text': 'First Step',
			},
		]

		if self.get_object():
			if self.get_object().is_step_one_complete():
				url = reverse('steps_2')
				active = True
			else:
				url = ''
				active = False
			steps.append(
                {
                    'active': active,
                    'url': url,
                    'text': 'Second Step',
                }
            )
			if self.get_object().is_step_two_complete():
				url = reverse('steps_3')
				active = True
			else:
				url = ''
				active = False
			steps.append(
				{
				    'active': active,
				    'url': url,
				    'text': 'Third Step',
				}
			)
		else:
			steps.append(
				{
				    'active': False,
				    'url': '',
				    'text': 'Second Step',
				}
			)
			steps.append(
				{
				    'active': False,
				    'url': '',
				    'text': 'Third Step',
				}
			)
		context.update({
			'prev_page_url': self.prev_page,
			'steps': steps,
		})
		return context

	def post(self, request, *args, **kwargs):

		if 'next' in self.request.POST:
			form = self.form_class(
				instance=self.get_object(),
				data=self.request.POST,
				user=self.request.user,
			)
			if form.is_valid():
				form.save()
		if 'logout' in self.request.POST:
			logout(request)
			return redirect(reverse(
	            'start_page',
	        ))

		return redirect(self.get_success_url())

	def get_success_url(self):
		return reverse(
		    self.next_page,
		)


class SecondStepPageView(
	StepPageView,
):
	form_class  = SecondStepForm
	prev_page = 'steps'
	next_page = 'steps_3'

	def dispatch(self, request, *args, **kwargs):
		user = self.request.user

		basic_info = BaseAccountModel.objects.filter(
			user=user
		).first()
		if basic_info:
			if not basic_info.is_step_one_complete():
				return redirect(reverse(
					'steps',
				))

		return super(SecondStepPageView, self).dispatch(request, *args, **kwargs)

class ThirdStepPageView(
	StepPageView,
):
	form_class  = ThirdStepForm
	prev_page = 'steps_2'
	next_page = 'landing_page'

	def dispatch(self, request, *args, **kwargs):
		user = self.request.user

		basic_info = BaseAccountModel.objects.filter(
			user=user
		).first()
		if basic_info:
			if not basic_info.is_step_two_complete():
				return redirect(reverse(
					'steps_2',
				))

		return super(ThirdStepPageView, self).dispatch(request, *args, **kwargs)


class AccountDataAjax(
    JsonRequestResponseMixin,
    AjaxResponseMixin,
    View,
):
	def get_ajax(self, request, *args, **kwargs):
		pk = request.GET.get('pk', None)

		user_data = BaseAccountModel.objects.get(pk=pk)
		data = {
			'f_name': user_data.first_name,
			'l_name': user_data.last_name,
			'adrress': user_data.address,
			'gender': user_data.gender,
			'date_of_birth': user_data.date_of_birth,
			'email': user_data.email,
		}

		return self.render_json_response(data)

	def post_ajax(self, request, *args, **kwargs):
		user = self.request.user

		basic_info = BaseAccountModel.objects.filter(
			user=user
		).first()

		if basic_info:
			form = BaseAccountForm(
				data=self.request.POST,
				instance=basic_info,
				user=user,
			)
		else:
			form = BaseAccountForm(
				data=self.request.POST,
				user=user,
			)

		if form.is_valid():
			person_data = form.save()
			return self.render_json_response({
				"status": "OK",
				"success": False,
				'name': person_data.full_name(),
				'adrress': person_data.address,
				'gender': person_data.get_gender_display(),
				'date_of_birth': person_data.date_of_birth.strftime("%b. %d, %Y"),
				'email': person_data.email,
			})
		else:
			error_dict = form.errors.as_json()
			return self.render_json_response({
				"status": "OK",
				"success": False,
				"message": error_dict
			})
