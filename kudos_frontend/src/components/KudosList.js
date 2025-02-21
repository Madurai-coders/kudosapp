import { useState, useEffect } from "react";
import apiService from "../services/apiService";
import KudosItem from "./KudosItem";

const KudosList = ({ currentUser }) => {
  const [kudos, setKudos] = useState([]);
  const [filter, setFilter] = useState("all"); // Default to showing all kudos
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch kudos based on filter
  useEffect(() => {
    const fetchKudos = async () => {
      setLoading(true);
      setError("");
      try {
        let endpoint = "/kudos/"; // Default: fetch all kudos
        if (filter === "received") {
          endpoint = "/kudos/received/";
        } else if (filter === "sent") {
          endpoint = "/kudos/given/";
        }

        const response = await apiService.get(endpoint);
        setKudos(response.data);
      } catch (err) {
        console.error("Error fetching kudos:", err);
        setError("Failed to load kudos.");
      } finally {
        setLoading(false);
      }
    };

    fetchKudos();
  }, [filter, currentUser?.id]); // Fetch when filter changes or user is loaded

  return (
    <div className="mt-6">
      {/* Error Message */}
      {error && <p className="text-red-500">{error}</p>}

      {/* Filter Buttons */} 
      <div className="flex gap-3 mb-4 justify-end mr-2">
        <button
          className={`px-4 py-2 rounded ${
            filter === "all" ? "bg-purple-600 text-white" : "bg-gray-700"
          }`}
          onClick={() => setFilter("all")}
        >
          All Kudos
        </button>
        <button
          className={`px-4 py-2 rounded ${
            filter === "received" ? "bg-blue-600 text-white" : "bg-gray-700"
          }`}
          onClick={() => setFilter("received")}
        >
          Received Kudos
        </button>
        <button
          className={`px-4 py-2 rounded ${
            filter === "sent" ? "bg-green-600 text-white" : "bg-gray-700"
          }`}
          onClick={() => setFilter("sent")}
        >
          Sent Kudos
        </button>
      </div>

      {/* Kudos List */}
      {loading ? (
        <p className="text-gray-400">Loading kudos...</p>
      ) : (
        <div className="space-y-3">
          {kudos.length > 0 ? (
            kudos.map((kudo) => <KudosItem key={kudo.id} kudo={kudo} />)
          ) : (
            <p className="text-gray-400">
              {filter === "all"
                ? "No kudos available."
                : filter === "received"
                ? "No kudos received yet."
                : "No kudos sent yet."}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default KudosList;
