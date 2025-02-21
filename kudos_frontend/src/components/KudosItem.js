import { capitalizeFirstLetter } from "../Utility/stringUtils";
import { format } from "date-fns"; // Import date-fns for formatting

const emojis = ["😊", "🎉", "👏", "🔥", "💪", "🌟", "🚀", "🙌", "🎊", "❤️"];

const getRandomEmoji = () => emojis[Math.floor(Math.random() * emojis.length)];

const KudosItem = ({ kudo }) => {
  const formattedTime = format(new Date(kudo.created_at), "PPpp"); // Example: Feb 20, 2025, 1:02 PM

  return (
    <div className="bg-gray-800 p-4 rounded-lg shadow-md mb-3 mr-4 relative">
      <p>
        <span className="text-blue-400 font-bold">
          {capitalizeFirstLetter(kudo.giver.username)}
        </span> 
        {" "}sent to{" "}
        <span className="text-green-400 font-bold">
          {capitalizeFirstLetter(kudo.receiver.username)}
        </span>:
      </p>
      <p className="italic text-gray-300">
        {getRandomEmoji()} "{kudo.message}" {getRandomEmoji()}
      </p>
      {/* Timestamp positioned at the bottom-right */}
      <p className="text-gray-400 text-xs absolute bottom-2 right-2">
        {formattedTime}
      </p>
    </div>
  );
};

export default KudosItem;
