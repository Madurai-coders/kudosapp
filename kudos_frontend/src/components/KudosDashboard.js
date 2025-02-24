import React, { useState, useEffect } from "react";
import apiService from "../services/apiService";
import KudosForm from "./KudosForm";
import KudosList from "./KudosList";

const KudosDashboard = ({ currentUser }) => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");
  const [message, setMessage] = useState("");
  const [kudosRemaining, setKudosRemaining] = useState(3);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [getKudos, setGetKudos] = useState(new Date());

  useEffect(() => {
    const fetchUsersAndQuota = async () => {
      try {
        const [userResponse, quotaResponse] = await Promise.all([
          apiService.get("/users/"),
          apiService.get("/user/quota/"),
        ]);

        setUsers(userResponse.data);
        setKudosRemaining(quotaResponse.data.kudos_remaining);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to load user data.");
      }
    };

    fetchUsersAndQuota();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (kudosRemaining <= 0) {
      alert("You have no kudos remaining for this week.");
      return;
    }
    setGetKudos(new Date());
    try {
      setLoading(true);
      await apiService.post("/kudos/", {
        receiver_id: selectedUser,
        message,
      });

      setKudosRemaining((prev) => prev - 1);
      setMessage("");
      alert("Kudos sent!");
    } catch (err) {
      console.error("Error sending kudos:", err);
      alert("Error sending kudos: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-52px)] flex items-start bg-black text-white p-10 pt-2">
      {/* Left: Fixed Kudos Form */}
      <div className="w-80 flex-shrink-0">
        <KudosForm
          users={users}
          selectedUser={selectedUser}
          setSelectedUser={setSelectedUser}
          message={message}
          setMessage={setMessage}
          kudosRemaining={kudosRemaining}
          handleSubmit={handleSubmit}
          loading={loading}
        />
      </div>

      {/* Right: Kudos List with API-based filtering */}
      <div className="flex-1 overflow-y-auto h-full scrollbar-thin scrollbar-thumb-blue-500 scrollbar-track-gray-900">
        <KudosList getKudos={getKudos}/>
      </div>
    </div>
  );
};

export default KudosDashboard;
