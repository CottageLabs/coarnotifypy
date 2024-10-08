from copy import deepcopy


class AnnounceRelationshipFixtureFactory:
    @classmethod
    def source(cls):
        return deepcopy(ANNOUNCE_RELATIONSHIP)


ANNOUNCE_RELATIONSHIP = {
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://purl.org/coar/notify"
    ],
    "actor": {
        "id": "https://research-organisation.org",
        "name": "Research Organisation",
        "type": "Organization"
    },
    "context": {
        "id": "https://another-research-organisation.org/repository/datasets/item/201203421/",
        "ietf:cite-as": "https://doi.org/10.5555/999555666",
        "ietf:item": {
            "id": "https://another-research-organisation.org/repository/datasets/item/201203421/data_archive.zip",
            "mediaType": "application/zip",
            "type": [
                "Article",
                "sorg:Dataset"
            ]
        },
        "type": "sorg:AboutPage"
    },
    "id": "urn:uuid:94ecae35-dcfd-4182-8550-22c7164fe23f",
    "object": {
        "as:object": "https://another-research-organisation.org/repository/datasets/item/201203421/",
        "as:relationship": "http://purl.org/vocab/frbr/core#supplement",
        "as:subject": "https://research-organisation.org/repository/item/201203/421/",
        "id": "urn:uuid:74FFB356-0632-44D9-B176-888DA85758DC",
        "type": "Relationship"
    },
    "origin": {
        "id": "https://research-organisation.org/repository",
        "inbox": "https://research-organisation.org/inbox/",
        "type": "Service"
    },
    "target": {
        "id": "https://another-research-organisation.org/repository",
        "inbox": "https://another-research-organisation.org/inbox/",
        "type": "Service"
    },
    "type": [
        "Announce",
        "coar-notify:RelationshipAction"
    ]
}