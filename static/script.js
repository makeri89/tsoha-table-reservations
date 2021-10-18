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

const format_review_value = () => {
  const rating = document.querySelector('#rating')
  const float = +rating.firstChild.data
  rating.textContent = float.toFixed(2)
}

const format_reservation_date = () => {
  const date = document.querySelector('#res_date')
  let formattedDate = date.textContent.split(' ')[0]
  formattedDate = formattedDate.split('-')
  formattedDate = `${formattedDate[2]}.${formattedDate[1]}.${formattedDate[0]}`
  date.textContent = formattedDate
}

const main = () => {
  if (window.location.href.includes('restaurants')) {
    format_review_value()
  } else if (window.location.href.includes('user')) {
    format_reservation_date()
  }
}

main()
