const makeReservationDayVisible = () => {
  const all = document.querySelectorAll(".reservation_date_picker");
  for (let i = 0; i < all.length; i++) {
    all[i].style.display = "none";
  }
  const datePicker = document.getElementById("date").value;
  const date = new Date(datePicker).getDay();
  const days = {
    0: ".sun",
    1: ".mon",
    2: ".tue",
    3: ".wed",
    4: ".thu",
    5: ".fri",
    6: ".sat",
  };
  const timeselector = document.querySelector(days[date]);
  timeselector.style.display = "block";
};

const response = new Response();
console.log(response.status);
