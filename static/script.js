const days = {
  0: '.sun',
  1: '.mon',
  2: '.tue',
  3: '.wed',
  4: '.thu',
  5: '.fri',
  6: '.sat',
}

const makeReservationDayVisible = () => {
  const notAvailable = document.querySelector('#daynotavailable')
  notAvailable.style.display = 'none'
  const all = document.querySelectorAll('.reservation_date_picker')
  all.forEach(d => (d.style.display = 'none'))
  const datePicker = document.getElementById('date').value
  const date = new Date(datePicker).getDay()
  const timeselector = document.querySelector(days[date])
  timeselector.style.display = 'block'
  if (timeselector.value === '') {
    notAvailable.style.display = 'block'
  }
}
