#----------------------------------------------------------------------
# Copyright (c) 2009-2011 Benito Jorge Bastida
# All rights reserved.
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#    o Redistributions of source code must retain the above copyright
#      notice, this list of conditions, and the disclaimer that follows.
#
#    o Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions, and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
#    o Neither the name of Digital Creations nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY DIGITAL CREATIONS AND CONTRIBUTORS *AS
#  IS* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#  PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL DIGITAL
#  CREATIONS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
#  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
#  DAMAGE.
#----------------------------------------------------------------------

import logging

from django import template
from django.conf import settings

from puzzlaef.dajaxice.core import DajaxiceRequest
from django.middleware.csrf import get_token

register = template.Library()

log = logging.getLogger('dajaxice')


@register.inclusion_tag('dajaxice/dajaxice_js_import.html', takes_context=True)
def dajaxice_js_import(context, core_url=None):
    # We must force this request to add the csrftoken cookie.
    request = context.get('request', None)
    if request:
        get_token(request)
    else:
        log.warning("The 'request' object must be accesible within the context. \
                     You must add 'django.contrib.messages.context_processors.request' \
                     to your TEMPLATE_CONTEXT_PROCESSORS and render your views\
                     using a RequestContext.")
    if not core_url or DajaxiceRequest.get_debug():
        core_url = '/%s/dajaxice.core.js' % DajaxiceRequest.get_media_prefix()
    else:
        core_url = '%s%s' % (settings.STATIC_URL or '', core_url,)
    return {'core_url': core_url}
