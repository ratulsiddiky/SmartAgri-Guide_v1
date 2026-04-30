def test_search_farms(client, monkeypatch):
    expected_farm_id = ObjectId()
    expected_doc = {
        "_id": expected_farm_id,
        "farm_name": "North Field",
        "crop_type": "Wheat",
    }

    class _FakeFarmsCollection:
        def count_documents(self, query):
           
            return 1 if "north" in str(query).lower() else 0
        
        def find(self, query):
            
            self.data = [expected_doc] if "north" in str(query).lower() else []
            return self
        
        def skip(self, n):
            return self
        
        def limit(self, n):

            return self.data

    monkeypatch.setattr(farms_routes, "_farms_collection", lambda: _FakeFarmsCollection())

    response = client.get("/api/farms/search?q=north")

    assert response.status_code == 200
    payload = response.get_json()
    
    assert payload["results_count"] == 1
    assert payload["total"] == 1
    assert payload["data"][0]["farm_name"] == "North Field"
    assert payload["data"][0]["_id"] == str(expected_farm_id)