const API_KEY = "34eb629903d82f7d11e930556dc585a2"; 
const BASE_URL = "https://api.openweathermap.org/data/2.5/weather";

const cityInput = document.getElementById("cityInput");
const searchBtn = document.getElementById("searchBtn");
const messageEl = document.getElementById("message");
const weatherBox = document.getElementById("weather");
const locationEl = document.getElementById("location");
const tempEl = document.getElementById("temp");
const humidityEl = document.getElementById("humidity");
const conditionEl = document.getElementById("condition");

async function getWeather(city) {
  messageEl.textContent = "";
  weatherBox.classList.add("hidden");

  if (!city) {
    messageEl.textContent = "Please enter a city name.";
    return;
  }

  const url = `${BASE_URL}?q=${encodeURIComponent(
    city
  )}&appid=${API_KEY}&units=metric`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      // 404, 401 etc.
      const errData = await response.json();
      messageEl.textContent =
        errData.message || "Could not fetch weather data.";
      return;
    }

    const data = await response.json();

    const locationText = `${data.name}, ${data.sys.country}`;
    const temp = data.main.temp;
    const humidity = data.main.humidity;
    const condition = data.weather[0].description;

    locationEl.textContent = locationText;
    tempEl.textContent = `Temperature: ${temp} °C`;
    humidityEl.textContent = `Humidity: ${humidity} %`;
    conditionEl.textContent = `Condition: ${condition}`;

    weatherBox.classList.remove("hidden");
  } catch (error) {
    console.error(error);
    messageEl.textContent = "Network error. Please try again.";
  }
}

searchBtn.addEventListener("click", () => {
  getWeather(cityInput.value.trim());
});

cityInput.addEventListener("keyup", (e) => {
  if (e.key === "Enter") {
    getWeather(cityInput.value.trim());
  }
});
