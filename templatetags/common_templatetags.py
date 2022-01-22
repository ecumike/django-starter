import re
import calendar
from math import log, floor

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from myapp.models import BannerNotification


register = template.Library()


@register.inclusion_tag('partials/banner_notification.html')
def bannerNotification():
	"""
	Gets all active banners and displays them at page top, 
	using the 'banner_notification.html' template.
	"""
	return {"banners": BannerNotification.objects.filter(active=True)}


@register.filter
def noprotocol(fullUrl):
	"""
	Strips protocol off URL for nice display/hotlink text.
	Example: https://www.someDomain.com/some/path/here/
	Return: {string} URL with no protocol (ex: www.someDomain.com/some/path/here/)
	"""
	returnData = re.sub(r"https?://", "", fullUrl)
	returnData = re.sub(r"/$", "", returnData)

	return returnData


##
## Global template HTML helpers for site consistency and easy redesigns.
##
@register.simple_tag(takes_context=True)
def getTemplateHelpers(context):
	
	horizontalSpace = 'ph3 ph4-ns'
	rounded = 'br2'
	
	commonButton = 'bo-button dib pointer ba bw0 ph4 pv3 bg-animate border-box ' + rounded
	smallButton = 'bo-smallbutton dib pointer ba bw0 pa2 bg-animate border-box ' + rounded
	
	tab = 'bo-tab w-100 pointer ph4 pv3 bw0 border-box b hover-white'
	
	icons = {
		'add': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon add"><defs><style>.cls-1{fill:none;}</style></defs><polygon points="17 15 17 7 15 7 15 15 7 15 7 17 15 17 15 25 17 25 17 17 25 17 25 15 17 15"/><rect class="cls-1" width="32" height="32"/></svg>',
		'arrowDown': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon"><defs><style>.cls-1{fill:none;}</style></defs><polygon points="24.59 16.59 17 24.17 17 2 15 2 15 24.17 7.41 16.59 6 18 16 28 26 18 24.59 16.59"/><rect class="cls-1" width="32" height="32"/></svg>',
		'checkmark': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon checkmark"><defs><style>.cls-1{fill:none;}</style></defs><path d="M16,2A14,14,0,1,0,30,16,14,14,0,0,0,16,2Zm0,26A12,12,0,1,1,28,16,12,12,0,0,1,16,28Z"/><polygon points="14 21.5 9 16.54 10.59 14.97 14 18.35 21.41 11 23 12.58 14 21.5"/><rect class="cls-1" width="32" height="32"/></svg>',
		'chevronForward': '<svg version="1.1" class="icon" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="7 0 32 32" style="enable-background:new 0 0 32 32;" xml:space="preserve"><style type="text/css">.st0{fill:none;}</style><polygon points="22,16 12,26 10.6,24.6 19.2,16 10.6,7.4 12,6 "/><rect id="_x3C_Transparent_Rectangle_x3E_" class="st0" width="32" height="32"/></svg>',
		'close': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="2 2 20 20" class="icon close"><g data-name="Layer 2"><g data-name="close"><rect width="24" height="24" transform="rotate(180 12 12)" opacity="0"/><path d="M13.41 12l4.3-4.29a1 1 0 1 0-1.42-1.42L12 10.59l-4.29-4.3a1 1 0 0 0-1.42 1.42l4.3 4.29-4.3 4.29a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0l4.29-4.3 4.29 4.3a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.42z"/></g></g></svg>',
		'document': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon"><defs><style>.cls-1{fill:none;}</style></defs><title>document</title><path d="M25.7,9.3l-7-7A.91.91,0,0,0,18,2H8A2,2,0,0,0,6,4V28a2,2,0,0,0,2,2H24a2,2,0,0,0,2-2V10A.91.91,0,0,0,25.7,9.3ZM18,4.4,23.6,10H18ZM24,28H8V4h8v6a2,2,0,0,0,2,2h6Z"/><rect x="11" y="22" width="10" height="2"/><rect x="11" y="16" width="10" height="2"/><rect class="cls-1" width="32" height="32"/></svg>',
		'edit': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon edit"><defs><style>.cls-1{fill:none;}</style></defs><rect x="2" y="27" width="28" height="2"/><path d="M25.41,9a2,2,0,0,0,0-2.83L21.83,2.59a2,2,0,0,0-2.83,0l-15,15V24h6.41Zm-5-5L24,7.59l-3,3L17.41,7ZM6,22V18.41l10-10L19.59,12l-10,10Z"/><rect class="cls-1" width="32" height="32"/></svg>',
		'email': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon email"><g data-name="Layer 2"><g data-name="email"><rect width="24" height="24" opacity="0"/><path d="M19 4H5a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h14a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3zm-.67 2L12 10.75 5.67 6zM19 18H5a1 1 0 0 1-1-1V7.25l7.4 5.55a1 1 0 0 0 .6.2 1 1 0 0 0 .6-.2L20 7.25V17a1 1 0 0 1-1 1z"/></g></g></svg>',
		'grid': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="2 -3 30 30" class="icon"><g data-name="Layer 2"><g data-name="grid"><rect width="24" height="24" opacity="0"/><path d="M9 3H5a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zM5 9V5h4v4z"/><path d="M19 3h-4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-4 6V5h4v4z"/><path d="M9 13H5a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2zm-4 6v-4h4v4z"/><path d="M19 13h-4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2zm-4 6v-4h4v4z"/></g></g></svg>',
		'help': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon help"><defs><style>.cls-1{fill:none;}</style></defs><title>help</title><path d="M16,2A14,14,0,1,0,30,16,14,14,0,0,0,16,2Zm0,26A12,12,0,1,1,28,16,12,12,0,0,1,16,28Z"/><circle cx="16" cy="23.5" r="1.5"/><path d="M17,8H15.5A4.49,4.49,0,0,0,11,12.5V13h2v-.5A2.5,2.5,0,0,1,15.5,10H17a2.5,2.5,0,0,1,0,5H15v4.5h2V17a4.5,4.5,0,0,0,0-9Z"/><rect class="cls-1" width="32" height="32"/></svg>',
		'info': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon info"><g data-name="Layer 2"><g data-name="info"><rect width="24" height="24" transform="rotate(180 12 12)" opacity="0"/><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/><circle cx="12" cy="8" r="1"/><path d="M12 10a1 1 0 0 0-1 1v5a1 1 0 0 0 2 0v-5a1 1 0 0 0-1-1z"/></g></g></svg>',
		'list': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon"><g data-name="Layer 2"><g data-name="list"><rect width="24" height="24" transform="rotate(180 12 12)" opacity="0"/><circle cx="4" cy="7" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="17" r="1"/><rect x="7" y="11" width="14" height="2" rx=".94" ry=".94"/><rect x="7" y="16" width="14" height="2" rx=".94" ry=".94"/><rect x="7" y="6" width="14" height="2" rx=".94" ry=".94"/></g></g></svg>',
		'modal': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon info"><g data-name="Layer 2"><g data-name="diagonal-arrow-right-up"><rect width="24" height="24" transform="rotate(180 12 12)" opacity="0"/><path d="M18 7.05a1 1 0 0 0-1-1L9 6a1 1 0 0 0 0 2h5.56l-8.27 8.29a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0L16 9.42V15a1 1 0 0 0 1 1 1 1 0 0 0 1-1z"/></g></g></svg>',
		'newWindow': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon new-window"><g data-name="Layer 2"><g data-name="external-link"><rect width="24" height="24" opacity="0"/><path d="M20 11a1 1 0 0 0-1 1v6a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h6a1 1 0 0 0 0-2H6a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3v-6a1 1 0 0 0-1-1z"/><path d="M16 5h1.58l-6.29 6.28a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0L19 6.42V8a1 1 0 0 0 1 1 1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-4a1 1 0 0 0 0 2z"/></g></g></svg>',
		'subtract': '<svg xmlns="http://www.w3.org/2000/svg" class="icon" x="0px" y="0px" viewBox="0 0 32 32" style="enable-background:new 0 0 32 32;" xml:space="preserve"><style type="text/css">.st0{fill:none;}</style><rect x="7" y="15" width="18" height="2"/><rect id="_x3C_Transparent_Rectangle_x3E_" class="st0" width="32" height="32"/></svg>',
		'time': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon time"><defs><style>.cls-1{fill:none;}</style></defs><title>time</title><path d="M16,30A14,14,0,1,1,30,16,14,14,0,0,1,16,30ZM16,4A12,12,0,1,0,28,16,12,12,0,0,0,16,4Z"/><polygon points="20.59 22 15 16.41 15 7 17 7 17 15.58 22 20.59 20.59 22"/><rect class="cls-1" width="32" height="32"/></svg>',
		'trash': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon trash"><defs><style>.cls-1{fill:none;}</style></defs><rect x="12" y="12" width="2" height="12"/><rect x="18" y="12" width="2" height="12"/><path d="M4,6V8H6V28a2,2,0,0,0,2,2H24a2,2,0,0,0,2-2V8h2V6ZM8,28V8H24V28Z"/><rect x="12" y="2" width="8" height="2"/><rect class="cls-1" width="32" height="32"/></svg>',
		'warn': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="icon warn"><defs><style>.cls-1{fill:none;}</style></defs><path d="M16,30A14,14,0,1,1,30,16,14,14,0,0,1,16,30ZM16,4A12,12,0,1,0,28,16,12,12,0,0,0,16,4Z"/><polygon points="20.59 22 15 16.41 15 7 17 7 17 15.58 22 20.59 20.59 22"/><rect class="cls-1" width="32" height="32"/></svg>',
	}
			
			
	return {
		'classes': {
			'button': commonButton,
			'smallButton': smallButton,
			'bluePriButton': 'ba bw1 b--blue bg-blue hover-bg-dark-blue hover-b--dark-blue white hover-white link',
			'blueSecButton': 'ba bw1 b--blue bg-white hover-bg-blue blue hover-white link',
			'greenPriButton': 'ba bw1 b--green bg-green hover-bg-dark-green hover-b--dark-green white hover-white link',
			'greenSecButton': 'ba bw1 b--green bg-white hover-bg-green green hover-white link',
			'redSecButton': 'ba bw1 b--dark-red bg-white hover-bg-dark-red dark-red hover-white link',
			'disabledButton': 'b--gray bg-black-10 black-40',
			'grid': horizontalSpace + ' w-100',
			'horizontalSpace': horizontalSpace,
			'hasIcon': 'inline-flex items-center underline-hover',
			'imageBorder': 'ba b--black-20',
			'link': 'link underline-hover',
			'navItem': 'light-blue pv3 link f6 f5-ns fw5 dib relative',
			'pageTitleSecondary': 'fw4 yellow',
			'rounded': rounded,
			'spinner': 'bo-spinner ba br-100',
			'tab': tab,
			'tableRowClickable': 'bg-animate hover-bg-lightest-blue pointer',
			'tableListCell': 'pv3 pr3 bb b--black-20 pl2',
			'tableListCell_bt': 'pv2 pr2 bt b--black-20',
			'tag': 'inline-flex items-center ba br2 b--moon-gray hover-b--blue hover-bg-blue textcolor hover-white pv1 ph2 mr2 mb2 f6 lh-solid bg-light-gray',
			'tooltipCue': 'bb b--black-20 b--dashed pointer normal bt-0 br-0 bl-0',
		},
		'html': {
			'hr': '<div class="w-100"><div class="bb b--silver"></div></div>',
			'icons': icons,
		}
	}


