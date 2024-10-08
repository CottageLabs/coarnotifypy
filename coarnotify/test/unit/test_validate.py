from unittest import TestCase
from copy import deepcopy

from coarnotify.models import NotifyDocument, NotifyService, NotifyObject, NotifyActor, NotifyItem
from coarnotify.models import (
    Accept,
    AnnounceEndorsement,
    AnnounceIngest,
    AnnounceRelationship,
    AnnounceReview,
    AnnounceServiceResult,
    RequestReview
)
from coarnotify.test.fixtures.notify import NotifyFixtureFactory
from coarnotify.test.fixtures import (
    AcceptFixtureFactory,
    AnnounceEndorsementFixtureFactory,
    AnnounceIngestFixtureFactory,
    AnnounceRelationshipFixtureFactory,
    AnnounceReviewFixtureFactory,
    AnnounceServiceResultFixtureFactory,
    RequestReviewFixtureFactory,
    URIFixtureFactory
)

from coarnotify.exceptions import ValidationError
from coarnotify.activitystreams2.activitystreams2 import Properties
from coarnotify.models.notify import NotifyProperties
from coarnotify import validate


class TestValidate(TestCase):
    def test_01_structural_empty(self):
        n = NotifyDocument()
        n.id = None     # these are automatically set, so remove them to trigger validation
        n.type = None
        with self.assertRaises(ValidationError) as ve:
            n.validate()

        errors = ve.exception.errors
        assert Properties.ID in errors
        assert Properties.TYPE in errors
        assert Properties.OBJECT in errors
        assert Properties.TARGET in errors
        assert Properties.ORIGIN in errors

    def test_02_structural_basic(self):
        n = NotifyDocument()
        with self.assertRaises(ValidationError) as ve:
            n.validate()

        errors = ve.exception.errors
        assert Properties.ID not in errors
        assert Properties.TYPE not in errors
        assert Properties.OBJECT in errors
        assert Properties.TARGET in errors
        assert Properties.ORIGIN in errors

    def test_03_structural_valid_document(self):
        n = NotifyDocument()
        n.target = NotifyFixtureFactory.target()
        n.origin = NotifyFixtureFactory.origin()
        n.object = NotifyFixtureFactory.object()

        assert n.validate() is True

    def test_04_structural_invalid_nested(self):
        n = NotifyDocument()
        n.target = NotifyService({"whatever": "value"}, validate_stream_on_construct=False)
        n.origin = NotifyService({"another": "junk"}, validate_stream_on_construct=False)
        n.object = NotifyObject({"yet": "more"}, validate_stream_on_construct=False)

        with self.assertRaises(ValidationError) as ve:
            n.validate()

        errors = ve.exception.errors
        assert Properties.ID not in errors
        assert Properties.TYPE not in errors
        assert Properties.OBJECT in errors
        assert Properties.TARGET in errors
        assert Properties.ORIGIN in errors

        target = errors[Properties.TARGET]
        assert len(target.get("errors")) == 0
        assert target.get("nested") is not None
        assert NotifyProperties.INBOX in target.get("nested")

        origin = errors[Properties.ORIGIN]
        assert len(origin.get("errors")) == 0
        assert origin.get("nested") is not None
        assert NotifyProperties.INBOX in origin.get("nested")

        object = errors[Properties.OBJECT]
        assert len(object.get("errors")) == 0
        assert object.get("nested") is not None
        assert Properties.TYPE in object.get("nested")

    def test_05_validation_modes(self):
        valid = NotifyFixtureFactory.source()
        n = NotifyDocument(stream=valid, validate_stream_on_construct=True)

        invalid = NotifyFixtureFactory.source()
        invalid["id"] = "http://example.com/^path"
        with self.assertRaises(ValidationError) as ve:
            n = NotifyDocument(stream=invalid, validate_stream_on_construct=True)
        assert ve.exception.errors.get(Properties.ID) is not None

        valid = NotifyFixtureFactory.source()
        n = NotifyDocument(stream=valid, validate_stream_on_construct=False)

        invalid = NotifyFixtureFactory.source()
        invalid["id"] = "http://example.com/^path"
        n = NotifyDocument(stream=invalid, validate_stream_on_construct=False)

        n = NotifyDocument(validate_properties=False)
        n.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"  # valid
        n.id = "http://example.com/^path"   # invalid

        with self.assertRaises(ValidationError) as ve:
            n.validate()
        assert ve.exception.errors.get(Properties.ID) is not None

    def test_06_validate_id_property(self):
        n = NotifyDocument()
        # test the various ways it can fail:
        with self.assertRaises(ValueError) as ve:
            n.id = "9whatever:none"
        assert ve.exception.args[0] == "Invalid URI scheme `9whatever`"

        with self.assertRaises(ValueError) as ve:
            n.id = "http://wibble/stuff"
        assert ve.exception.args[0] == "Invalid URI authority `wibble`"

        with self.assertRaises(ValueError) as ve:
            n.id = "http://example.com/^path"
        assert ve.exception.args[0] == "Invalid URI path `/^path`"

        with self.assertRaises(ValueError) as ve:
            n.id = "http://example.com/path/here/?^=what"
        assert ve.exception.args[0] == "Invalid URI query `^=what`"

        with self.assertRaises(ValueError) as ve:
            n.id = "http://example.com/path/here/?you=what#^frag"
        assert ve.exception.args[0] == "Invalid URI fragment `^frag`"

        # test a bunch of successful ones

        # These ones taken from wikipedia
        n.id = "https://john.doe@www.example.com:1234/forum/questions/?tag=networking&order=newest#top"
        n.id = "https://john.doe@www.example.com:1234/forum/questions/?tag=networking&order=newest#:~:text=whatever"
        n.id = "ldap://[2001:db8::7]/c=GB?objectClass?one"
        n.id = "mailto:John.Doe@example.com"
        n.id = "news:comp.infosystems.www.servers.unix"
        n.id = "tel:+1-816-555-1212"
        n.id = "telnet://192.0.2.16:80/"
        n.id = "urn:oasis:names:specification:docbook:dtd:xml:4.1.2"

        # these ones taken from the spec
        n.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"
        n.id = "https://generic-service.com/system"
        n.id = "https://generic-service.com/system/inbox/"

    def test_07_validate_url(self):
        urls = URIFixtureFactory.generate(schemes=["http", "https"])
        # print(urls)

        for url in urls:
            # print(url)
            assert validate.url(None, url) is True

        with self.assertRaises(ValueError):
            validate.url(None, "ftp://example.com")
        with self.assertRaises(ValueError):
            validate.url(None, "http:/example.com")
        with self.assertRaises(ValueError):
            validate.url(None, "http://domain/path")
        with self.assertRaises(ValueError):
            validate.url(None, "http://example.com/path^wrong")

    def test_08_one_of(self):
        values = ["a", "b", "c"]
        validator = validate.one_of(values)
        assert validator(None, "a") is True
        assert validator(None, "b") is True
        assert validator(None, "c") is True

        with self.assertRaises(ValueError):
            validator(None, "d")

        actor = NotifyActor()
        with self.assertRaises(ValueError):
            actor.type = "SomethingElse"

        source = AnnounceEndorsementFixtureFactory.source()
        asource = source.get("actor")
        asource["type"] = "SomethingElse"
        with self.assertRaises(ValidationError):
            NotifyActor(asource, validation_context=Properties.ACTOR)

        source = AnnounceEndorsementFixtureFactory.source()
        source["actor"]["type"] = "SomethingElse"
        with self.assertRaises(ValidationError):
            AnnounceEndorsement(source)

    def test_09_contains(self):
        validator = validate.contains("a")
        assert validator(None, ["a", "b", "c"]) is True

        with self.assertRaises(ValueError):
            validator(None, ["b", "c", "d"])

        source = AnnounceEndorsementFixtureFactory.source()
        osource = source.get("origin")
        osource["type"] = "SomethingElse"
        with self.assertRaises(ValidationError):
            NotifyActor(osource, validation_context=Properties.ORIGIN)

        source = AnnounceEndorsementFixtureFactory.source()
        source["origin"]["type"] = "SomethingElse"
        with self.assertRaises(ValidationError):
            AnnounceEndorsement(source)

    ########################################
    ## validation methods for specific patterns

    def _base_validate(self, a):
        # now try to apply invalid values to it
        with self.assertRaises(ValueError):
            a.id = "not a uri"

        with self.assertRaises(ValueError):
            a.in_reply_to = "not a uri"

        with self.assertRaises(ValueError):
            # not an HTTP URI
            a.origin.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"

        with self.assertRaises(ValueError):
            a.origin.inbox = "not a uri"

        with self.assertRaises(ValueError):
            a.origin.type = "NotAValidType"

        with self.assertRaises(ValueError):
            # not an HTTP URI
            a.target.id = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"

        with self.assertRaises(ValueError):
            a.target.inbox = "not a uri"

        with self.assertRaises(ValueError):
            a.target.type = "NotAValidType"

        with self.assertRaises(ValueError):
            a.type = "NotAValidType"

    def _actor_validate(self, a):
        with self.assertRaises(ValueError):
            a.actor.id = "not a uri"

        with self.assertRaises(ValueError):
            a.actor.type = "NotAValidType"

    def _object_validate(self, a):
        with self.assertRaises(ValueError):
            a.object.id = "not a uri"

        with self.assertRaises(ValueError):
            a.object.cite_as = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"

    def _context_validate(self, a):
        with self.assertRaises(ValueError):
            a.context.id = "not a uri"

        with self.assertRaises(ValueError):
            a.context.type = "NotAValidType"

        with self.assertRaises(ValueError):
            a.context.cite_as = "urn:uuid:4fb3af44-d4f8-4226-9475-2d09c2d8d9e0"

    def test_10_accept_validate(self):
        # make a valid one
        source = AcceptFixtureFactory.source()
        a = Accept(source)

        self._base_validate(a)

        # now make one with fully invalid data
        isource = AcceptFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = Accept(isource)

    def test_11_announce_endorsement_validate(self):
        # make a valid one
        source = AnnounceEndorsementFixtureFactory.source()
        a = AnnounceEndorsement(source)

        self._base_validate(a)

        with self.assertRaises(ValueError):
            # one of the required types, but not both of them
            a.type = "Announce"

        self._actor_validate(a)
        self._object_validate(a)
        self._context_validate(a)

        # now make one with fully invalid data
        isource = AnnounceEndorsementFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = AnnounceEndorsement(isource)

    def test_19_announce_review_validate(self):
        # make a valid one
        source = RequestReviewFixtureFactory.source()
        a = RequestReview(source)

        self._base_validate(a)

        with self.assertRaises(ValueError):
            # one of the required types, but not both of them
            a.type = "Offer"

        self._actor_validate(a)
        self._object_validate(a)

        # now make one with fully invalid data
        isource = RequestReviewFixtureFactory.invalid()
        with self.assertRaises(ValidationError) as ve:
            a = RequestReview(isource)
