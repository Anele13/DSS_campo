// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

(function(Chart) {
	var helpers = Chart.helpers;

	Chart.defaults.barFunnel = {
		hover: {
			mode: "label"
		},

		region: {
			display: true,
			borderColor: "#F6C85F",
			backgroundColor: "rgba(246, 200, 95, 0.2)"
		},

		elements: {
			rectangle: {
				stepLabel: {
					display: true,
					fontSize: 5
				}
			}
		},

		scales: {
			xAxes: [{
				type: "category",

				// Specific to Bar Controller
				categoryPercentage: 0.8,
				barPercentage: 0.7,

				// grid line settings
				gridLines: {
					offsetGridLines: true
				}
			}],
			yAxes: [{
				type: "linear"
			}]
		},
		tooltips: {
			backgroundColor: "rgb(255,255,255)",
			bodyFontColor: "#858796",
			titleMarginBottom: 10,
			titleFontColor: '#6e707e',
			titleFontSize: 14,
			borderColor: '#dddfeb',
			borderWidth: 1,
			xPadding: 15,
			yPadding: 15,
			displayColors: false,
			intersect: false,
			mode: 'index',
			caretPadding: 10,
			callbacks: {
			  label: function(tooltipItem, chart) {
				var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
				return datasetLabel + ':'+tooltipItem.yLabel;
			  }
			}
		  }
	};

	Chart.controllers.barFunnel = Chart.controllers.bar.extend({
		updateElement: function updateElement(rectangle, index, reset, numBars) {
			var meta = this.getMeta();
			var xScale = this.getScaleForId(meta.xAxisID);
			var yScale = this.getScaleForId(meta.yAxisID);

			var yScalePoint;

			if (yScale.min < 0 && yScale.max < 0) {
				// all less than 0. use the top
				yScalePoint = yScale.getPixelForValue(yScale.max);
			} else if (yScale.min > 0 && yScale.max > 0) {
				yScalePoint = yScale.getPixelForValue(yScale.min);
			} else {
				yScalePoint = yScale.getPixelForValue(0);
			}

			var chartOptions = this.chart.options;
			var rectangleElementOptions = this.chart.options.elements.rectangle;
			var custom = rectangle.custom || {};
			var dataset = this.getDataset();
      var ruler = this.getRuler(this.index);

			helpers.extend(rectangle, {
				// Utility
				_chart: this.chart.chart,
				_xScale: xScale,
				_yScale: yScale,
				_datasetIndex: this.index,
				_index: index,


				// Desired view properties
				_model: {
					x: this.calculateBarX(index, this.index, ruler),
					y: reset ? yScalePoint : this.calculateBarY(index, this.index),

					// Tooltip
					label: this.chart.data.labels[index],
					datasetLabel: dataset.label,

					// Appearance
					base: reset ? yScalePoint : this.calculateBarBase(this.index, index),
					width: this.calculateBarWidth(ruler),
					backgroundColor: custom.backgroundColor ? custom.backgroundColor : helpers.getValueAtIndexOrDefault(dataset.backgroundColor, index, rectangleElementOptions.backgroundColor),
					borderSkipped: custom.borderSkipped ? custom.borderSkipped : rectangleElementOptions.borderSkipped,
					borderColor: custom.borderColor ? custom.borderColor : helpers.getValueAtIndexOrDefault(dataset.borderColor, index, rectangleElementOptions.borderColor),
					borderWidth: custom.borderWidth ? custom.borderWidth : helpers.getValueAtIndexOrDefault(dataset.borderWidth, index, rectangleElementOptions.borderWidth),
					stepLabelColor: rectangleElementOptions.stepLabel.color ? rectangleElementOptions.stepLabel.color : helpers.getValueAtIndexOrDefault(dataset.borderColor, index, rectangleElementOptions.borderColor),
					stepLabelFontSize: rectangleElementOptions.stepLabel.fontSize ? rectangleElementOptions.stepLabel.fontSize : chartOptions.defaultFontSize
				},

				draw: function () {

					var ctx = this._chart.ctx;
					var vm = this._view;
					var options = this._chart.config.options;

					var halfWidth = vm.width / 2,
						leftX = vm.x - halfWidth,
						rightX = vm.x + halfWidth,
						top = vm.base - (vm.base - vm.y),
						halfStroke = vm.borderWidth / 2;

					// Canvas doesn't allow us to stroke inside the width so we can
					// adjust the sizes to fit if we're setting a stroke on the line
					if (vm.borderWidth) {
						leftX += halfStroke;
						rightX -= halfStroke;
						top += halfStroke;
					}

					ctx.beginPath();
					ctx.fillStyle = vm.backgroundColor;
					ctx.strokeStyle = vm.borderColor;
					ctx.lineWidth = vm.borderWidth;

					// Corner points, from bottom-left to bottom-right clockwise
					// | 1 2 |
					// | 0 3 |
					var corners = [
						[leftX, vm.base],
						[leftX, top],
						[rightX, top],
						[rightX, vm.base]
					];

					// Find first (starting) corner with fallback to 'bottom'
					var borders = ['bottom', 'left', 'top', 'right'];
					var startCorner = borders.indexOf(vm.borderSkipped, 0);
					if (startCorner === -1)
						startCorner = 0;

					function cornerAt(index) {
						return corners[(startCorner + index) % 4];
					}

					// Draw rectangle from 'startCorner'
					ctx.moveTo.apply(ctx, cornerAt(0));
					for (var i = 1; i < 4; i++)
						ctx.lineTo.apply(ctx, cornerAt(i));

					ctx.fill();
					if (vm.borderWidth) {
						ctx.stroke();
					}

					if(rectangleElementOptions.stepLabel.display && (index != 0)) {
						var label = (dataset.data[index] / dataset.data[0]) * 100;

						if (dataset.data[index] > 0) {
							// Draw Step Label
							ctx.font = vm.stepLabelFontSize + "px " + options.defaultFontFamily;
							ctx.fillStyle = vm.stepLabelColor;
							ctx.textAlign = "center";
							ctx.fillText(label.toFixed(0) + "%", vm.x, vm.y - vm.stepLabelFontSize);
						}
					}

					if (chartOptions.region.display && (index < meta.data.length - 1)) {
						var nextVm = meta.data[index + 1]._view;

						var regionCorners = [
							[vm.x + halfWidth, top],
							[nextVm.x - halfWidth, nextVm.base - (nextVm.base - nextVm.y - 1)],
							[nextVm.x - halfWidth, nextVm.base],
							[vm.x + halfWidth, vm.base]
						];

						ctx.beginPath();
						ctx.strokeStyle = chartOptions.region.borderColor;
						ctx.moveTo.apply(ctx, regionCorners[0]);
						ctx.lineTo.apply(ctx, regionCorners[1]);
						ctx.stroke();

						ctx.beginPath();
						ctx.strokeStyle = "transparent";
						ctx.fillStyle = chartOptions.region.backgroundColor;
						ctx.moveTo.apply(ctx, regionCorners[1]);
						ctx.lineTo.apply(ctx, regionCorners[2]);
						ctx.lineTo.apply(ctx, regionCorners[3]);
						ctx.lineTo.apply(ctx, regionCorners[0]);
						ctx.fill();
						ctx.stroke();
					}

				}
			});
			rectangle.pivot();
		}
	});
}).call(this, Chart);
