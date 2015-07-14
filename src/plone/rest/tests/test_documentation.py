# -*- coding: utf-8 -*-
from plone.rest.testing import PLONE_REST_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.textfield.value import RichTextValue

import unittest
import requests

HEADER_KEYS = [
    'allow',
    'content-type',
]


def save_response_for_documentation(filename, response):
    f = open('../../docs/source/_json/%s' % filename, 'w')
    f.write('{} {}\n'.format(
        response.request.method,
        response.request.path_url
    ))
    f.write('\n')
    f.write('HTTP {} {}\n'.format(response.status_code, response.reason))
    for key, value in response.headers.items():
        if key.lower() in HEADER_KEYS:
            f.write('{}: {}\n'.format(key, value))
    f.write('\n')
    f.write(response.content)
    f.close()


class TestTraversal(unittest.TestCase):

    layer = PLONE_REST_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', id='front-page')
        self.document = self.portal['front-page']
        self.document.title = u"Welcome to Plone"
        self.document.description = \
            u"Congratulations! You have successfully installed Plone."
        self.document.text = RichTextValue(
            u"If you're seeing this instead of the web site you were " +
            u"expecting, the owner of this web site has just installed " +
            u"Plone. Do not contact the Plone Team or the Plone mailing " +
            u"lists about this.",
            'text/plain',
            'text/html'
        )
        import transaction
        transaction.commit()

    def test_documentation_document(self):
        response = requests.get(
            self.document.absolute_url(),
            headers={
                'Accept': 'application/json'
            },
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        save_response_for_documentation('document.json', response)

    def test_documentation_siteroot_get(self):
        response = requests.get(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        save_response_for_documentation('siteroot-get.json', response)

    def test_documentation_siteroot_post(self):
        response = requests.post(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        save_response_for_documentation('siteroot-post.json', response)

    def test_documentation_siteroot_delete(self):
        response = requests.delete(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        save_response_for_documentation('siteroot-delete.json', response)

    def test_documentation_siteroot_put(self):
        response = requests.put(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        save_response_for_documentation('siteroot-put.json', response)

    def test_documentation_siteroot_patch(self):
        response = requests.patch(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        save_response_for_documentation('siteroot-patch.json', response)

    def test_documentation_siteroot_options(self):
        response = requests.options(
            self.portal.absolute_url(),
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        save_response_for_documentation('siteroot-options.json', response)
