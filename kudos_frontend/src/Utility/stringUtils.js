export const capitalizeFirstLetter = (str) => {
    if (!str) return str; // Handle null or undefined
    return str.charAt(0).toUpperCase() + str.slice(1);
  };