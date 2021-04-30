// Other important pens.
// Map: https://codepen.io/themustafaomar/pen/ZEGJeZq
// Navbar: https://codepen.io/themustafaomar/pen/VKbQyZ

'use strict'

function $(selector) {
	return document.querySelector(selector)
}

function find(el, selector) {
	let finded
	return (finded = el.querySelector(selector)) ? finded : null
}

function siblings(el) {
	const siblings = []
	for (let sibling of el.parentNode.children) {
		if (sibling !== el) {
			siblings.push(sibling)
		}
	}
	return siblings
}

const showAsideBtn = $('.show-side-btn')
const sidebar = $('.sidebar')
const wrapper = $('#wrapper')

showAsideBtn.addEventListener('click', function () {
	$(`#${this.dataset.show}`).classList.toggle('show-sidebar')
	wrapper.classList.toggle('fullwidth')
})

if (window.innerWidth < 767) {
	sidebar.classList.add('show-sidebar');
}

window.addEventListener('resize', function () {
	if (window.innerWidth > 767) {
		sidebar.classList.remove('show-sidebar')
	}
})

// dropdown menu in the side nav
var slideNavDropdown = $('.sidebar-dropdown');

$('.sidebar .categories').addEventListener('click', function (event) {
	// event.preventDefault()

	const item = event.target.closest('.has-dropdown')

	if (item) {
		item.classList.toggle('opened')

		siblings(item).forEach(sibling => {
			sibling.classList.remove('opened')
		})
	
		if (item.classList.contains('opened')) {
			const toOpen = find(item, '.sidebar-dropdown')

			if (toOpen) {
				toOpen.classList.add('active')
			}
	
			siblings(item).forEach(sibling => {
				const toClose = find(sibling, '.sidebar-dropdown')

				if (toClose) {
					toClose.classList.remove('active')
				}
			})
		} else {
			find(item, '.sidebar-dropdown').classList.toggle('active')
		}
	}
})

$('.sidebar .close-aside').addEventListener('click', function () {
	$(`#${this.dataset.close}`).classList.add('show-sidebar')
	wrapper.classList.remove('margin')
})


// The bar chart
var myChart = new Chart(document.getElementById('myChart'), {
	type: 'bar',
	data: {
		labels: ["January", "February", "March", "April", 'May', 'June', 'August', 'September'],
		datasets: [{
			label: "Lost",
			data: [45, 25, 40, 20, 60, 20, 35, 25],
			backgroundColor: "#0d6efd",
			borderColor: 'transparent',
			borderWidth: 2.5,
			barPercentage: 0.4,
		}, {
			label: "Succes",
			startAngle: 2,
			data: [20, 40, 20, 50, 25, 40, 25, 10],
			backgroundColor: "#dc3545",
			borderColor: 'transparent',
			borderWidth: 2.5,
			barPercentage: 0.4,
		}]
	},
	options: {
		scales: {
			yAxes: [{
				gridLines: {},
				ticks: {
					stepSize: 15,
				},
			}],
			xAxes: [{
				gridLines: {
					display: false,
				}
			}]
		}
	}
})

// The line chart
var chart = new Chart(document.getElementById('myChart2'), {
	type: 'line',
	data: {
		labels: ["January", "February", "March", "April", 'May', 'June', 'August', 'September'],
		datasets: [{
			label: "My First dataset",
			data: [4, 20, 5, 20, 5, 25, 9, 18],
			backgroundColor: 'transparent',
			borderColor: '#0d6efd',
			lineTension: .4,
			borderWidth: 1.5,
		}, {
			label: "Month",
			data: [11, 25, 10, 25, 10, 30, 14, 23],
			backgroundColor: 'transparent',
			borderColor: '#dc3545',
			lineTension: .4,
			borderWidth: 1.5,
		}, {
			label: "Month",
			data: [16, 30, 16, 30, 16, 36, 21, 35],
			backgroundColor: 'transparent',
			borderColor: '#f0ad4e',
			lineTension: .4,
			borderWidth: 1.5,
		}]
	},
	options: {
		scales: {
			yAxes: [{
				gridLines: {
					drawBorder: false
				},
				ticks: {
					stepSize: 12,
				}
			}],
			xAxes: [{
				gridLines: {
					display: false,
				},
			}]
		}
	}
})

var chart = document.getElementById('chart3');
var myChart = new Chart(chart, {
	type: 'line',
	data: {
		labels: ["One", "Two", "Three", "Four", "Five", 'Six', "Seven", "Eight"],
		datasets: [{
			label: "Lost",
			lineTension: 0.2,
			borderColor: '#d9534f',
			borderWidth: 1.5,
			showLine: true,
			data: [3, 30, 16, 30, 16, 36, 21, 40, 20, 30],
			backgroundColor: 'transparent'
		}, {
			label: "Lost",
			lineTension: 0.2,
			borderColor: '#5cb85c',
			borderWidth: 1.5,
			data: [6, 20, 5, 20, 5, 25, 9, 18, 20, 15],
			backgroundColor: 'transparent'
		},
		{
			label: "Lost",
			lineTension: 0.2,
			borderColor: '#f0ad4e',
			borderWidth: 1.5,
			data: [12, 20, 15, 20, 5, 35, 10, 15, 35, 25],
			backgroundColor: 'transparent'
		},
		{
			label: "Lost",
			lineTension: 0.2,
			borderColor: '#337ab7',
			borderWidth: 1.5,
			data: [16, 25, 10, 25, 10, 30, 14, 23, 14, 29],
			backgroundColor: 'transparent'
		}]
	},
	options: {
		scales: {
			yAxes: [{
				gridLines: {
					drawBorder: false
				},
				ticks: {
					stepSize: 12
				}
			}],
			xAxes: [{
				gridLines: {
					display: false,
				},
			}],
		}
	}
})