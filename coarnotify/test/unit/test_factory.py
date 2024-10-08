from unittest import TestCase

from coarnotify.models import (
    Accept,
    AnnounceEndorsement,
    AnnounceIngest,
    AnnounceRelationship,
    AnnounceReview,
    AnnounceServiceResult,
    Reject,
    RequestEndorsement,
    RequestIngest,
    RequestReview
)
from coarnotify.common import COARNotifyFactory

from coarnotify.test.fixtures import (
    AcceptFixtureFactory,
    AnnounceEndorsementFixtureFactory,
    AnnounceIngestFixtureFactory,
    AnnounceRelationshipFixtureFactory,
    AnnounceReviewFixtureFactory,
    AnnounceServiceResultFixtureFactory,
    RejectFixtureFactory,
    RequestEndorsementFixtureFactory,
    RequestIngestFixtureFactory,
    RequestReviewFixtureFactory
)


class TestFactory(TestCase):
    def test_01_accept(self):
        acc = COARNotifyFactory.get_by_types(Accept.TYPE)
        assert acc == Accept

        source = AcceptFixtureFactory.source()
        acc = COARNotifyFactory.get_by_object(source)
        assert isinstance(acc, Accept)

        assert acc.id == source["id"]

    def test_02_announce_endorsement(self):
        ae = COARNotifyFactory.get_by_types(AnnounceEndorsement.TYPE)
        assert ae == AnnounceEndorsement

        source = AnnounceEndorsementFixtureFactory.source()
        ae = COARNotifyFactory.get_by_object(source)
        assert isinstance(ae, AnnounceEndorsement)

        assert ae.id == source["id"]

    def test_03_announce_ingest(self):
        ai = COARNotifyFactory.get_by_types(AnnounceIngest.TYPE)
        assert ai == AnnounceIngest

        source = AnnounceIngestFixtureFactory.source()
        ai = COARNotifyFactory.get_by_object(source)
        assert isinstance(ai, AnnounceIngest)

        assert ai.id == source["id"]

    def test_04_announce_relationship(self):
        ar = COARNotifyFactory.get_by_types(AnnounceRelationship.TYPE)
        assert ar == AnnounceRelationship

        source = AnnounceRelationshipFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, AnnounceRelationship)

        assert ar.id == source["id"]

    def test_05_announce_review(self):
        ar = COARNotifyFactory.get_by_types(AnnounceReview.TYPE)
        assert ar == AnnounceReview

        source = AnnounceReviewFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, AnnounceReview)

        assert ar.id == source["id"]

    def test_06_announce_service_result(self):
        ar = COARNotifyFactory.get_by_types(AnnounceServiceResult.TYPE)
        assert ar == AnnounceServiceResult

        source = AnnounceServiceResultFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, AnnounceServiceResult)

        assert ar.id == source["id"]

    def test_07_reject(self):
        ar = COARNotifyFactory.get_by_types(Reject.TYPE)
        assert ar == Reject

        source = RejectFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, Reject)

        assert ar.id == source["id"]

    def test_08_request_endorsement(self):
        ar = COARNotifyFactory.get_by_types(RequestEndorsement.TYPE)
        assert ar == RequestEndorsement

        source = RequestEndorsementFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, RequestEndorsement)

        assert ar.id == source["id"]

    def test_09_request_ingest(self):
        ar = COARNotifyFactory.get_by_types(RequestIngest.TYPE)
        assert ar == RequestIngest

        source = RequestIngestFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, RequestIngest)

        assert ar.id == source["id"]

    def test_10_request_review(self):
        ar = COARNotifyFactory.get_by_types(RequestReview.TYPE)
        assert ar == RequestReview

        source = RequestReviewFixtureFactory.source()
        ar = COARNotifyFactory.get_by_object(source)
        assert isinstance(ar, RequestReview)

        assert ar.id == source["id"]
