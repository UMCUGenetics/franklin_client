def test_get_assay_list(franklin):
    assert franklin.get_assay_list() == [
        {"id": "7606dc0q-2e93-4967-9e4b-db85b128c5da", "name": "Exome"},
        {"id": "bd0bf7eb-557d-4581-bc76-6bcef59a355a", "name": "Panel"}
    ]


def test_get_analysis_list(franklin):
    assert franklin.get_analysis_list()['0e8389ee-b6ee-41f0-8eca-093e115e7064'] == [217, 183]


def test_get_analysis_status(franklin):
    assert franklin.get_analysis_status([17, 18, 19]) == [
        {
            "id": 17,
            "name": "Demo Sample 1",
            "status": "ACTIVE",
            "assay_id": "620434fa-e367-425a-vbnb-n3g7ha10c7a",
            "created_at": "2018-10-01"
        },
        {
            "id": 18,
            "name": "Demo Sample 2",
            "status": "ACTIVE",
            "assay_id": "620434fa-e367-425a-vbnb-n3g7ha10c7a",
            "created_at": "2018-10-02"
        },
        {
            "id": 19,
            "name": "Demo sample 3",
            "status": "ACTIVE",
            "assay_id": "620434fa-e367-425a-vbnb-n3g7ha10c7a",
            "created_at": "2018-10-02"
        }
    ]
