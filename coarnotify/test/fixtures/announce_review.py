from copy import deepcopy


class AnnounceReviewFixtureFactory:
    @classmethod
    def source(cls):
        return deepcopy(ANNOUNCE_REVIEW)


ANNOUNCE_REVIEW = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://purl.org/coar/notify"
    ],
    "actor": {
        "id": "https://review-service.com",
        "name": "Review Service",
        "type": "Service"
    },
    "context": {
        "id": "https://research-organisation.org/repository/preprint/201203/421/",
        "ietf:cite-as": "https://doi.org/10.5555/12345680",
        "ietf:item": {
            "id": "https://research-organisation.org/repository/preprint/201203/421/content.pdf",
            "mediaType": "application/pdf",
            "type": [
                "Article",
                "sorg:ScholarlyArticle"
            ]
        },
        "type": "sorg:AboutPage"
    },
    "id": "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f",
    "inReplyTo": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
    "object": {
        "id": "https://review-service.com/review/geo/202103/0021",
        "ietf:cite-as": "https://doi.org/10.3214/987654",
        "type": [
            "Document",
            "sorg:Review"
        ]
    },
    "origin": {
        "id": "https://review-service.com/system",
        "inbox": "https://review-service.com/inbox/",
        "type": "Service"
    },
    "target": {
        "id": "https://generic-service.com/system",
        "inbox": "https://generic-service.com/system/inbox/",
        "type": "Service"
    },
    "type": [
        "Announce",
        "coar-notify:ReviewAction"
    ]
}

