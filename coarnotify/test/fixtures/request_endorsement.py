from copy import deepcopy


class RequestEndorsementFixtureFactory:
    @classmethod
    def source(cls):
        return deepcopy(REQUEST_ENDORSEMENT)


REQUEST_ENDORSEMENT = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://purl.org/coar/notify"
    ],
    "actor": {
        "id": "https://orcid.org/0000-0002-1825-0097",
        "name": "Josiah Carberry",
        "type": "Person"
    },
    "id": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
    "object": {
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
    "origin": {
        "id": "https://research-organisation.org/repository",
        "inbox": "https://research-organisation.org/inbox/",
        "type": "Service"
    },
    "target": {
        "id": "https://overlay-journal.com/system",
        "inbox": "https://overlay-journal.com/inbox/",
        "type": "Service"
    },
    "type": [
        "Offer",
        "coar-notify:EndorsementAction"
    ]
}