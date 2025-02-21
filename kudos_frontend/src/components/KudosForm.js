import React, { useMemo } from "react";

const KudosForm = ({ 
  users, selectedUser, setSelectedUser, 
  message, setMessage, kudosRemaining, 
  handleSubmit, loading 
}) => {
  // Check if the kudos reset is near
  const isResetSoon = useMemo(() => {
    const now = new Date();
    const day = now.getDay(); // 0 = Sunday, 6 = Saturday
    const hours = now.getHours();
    
    // If today is Thursday (day 4) or later, show reset warning
    return (day >= 4) || (day === 0 && hours < 1);
  }, []);

  return (
    <form 
      onSubmit={handleSubmit} 
      className="fixed top-35 left-4 w-80 bg-gray-900 p-4 rounded-xl shadow-lg"
    >
      <h2 className="text-lg font-bold text-center mb-3 text-white">Give Kudos</h2>

      {/* Select User */}
      <div className="mb-3">
        <label className="block text-gray-400 text-sm">Select User:</label>
        <select
          className="w-full p-2 mt-1 bg-gray-800 text-white border border-gray-600 rounded-md 
                     focus:ring-2 focus:ring-blue-500 text-sm"
          onChange={(e) => setSelectedUser(e.target.value)}
          value={selectedUser}
          required
        >
          <option value="">Select a user</option>
          {users.map((user) => (
            <option key={user.id} value={user.id}>{user.username}</option>
          ))}
        </select>
      </div>

      {/* Message Input */}
      <div className="mb-3">
        <label className="block text-gray-400 text-sm">Message:</label>
        <textarea
          className="w-full p-2 mt-1 bg-gray-800 text-white border border-gray-600 rounded-md 
                     focus:ring-2 focus:ring-blue-500 text-sm"
          onChange={(e) => setMessage(e.target.value)}
          value={message}
          rows="2"
          required
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 
                   rounded-md transition-all disabled:bg-gray-600 text-sm"
        disabled={loading || kudosRemaining <= 0}  // Disable if no kudos left
      >
        {loading ? "Sending..." : "Send Kudos"}
      </button>

      {/* Kudos Remaining */}
      <p className="text-center mt-2 text-gray-400 text-xs">
        Kudos Remaining: <span className="text-blue-400">{kudosRemaining}</span>
      </p>

      {/* Reset Warning */}
      {isResetSoon && kudosRemaining > 0 && (
        <p className="text-red-400 text-xs text-center mt-1 font-semibold">
          ⚠️ Kudos will reset soon!
        </p>
      )}
    </form>
  );
};

export default KudosForm;
