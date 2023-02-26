<script lang="ts">
	import { Card } from 'flowbite-svelte';
	import FusionCharts from 'fusioncharts';
	import Widgets from 'fusioncharts/fusioncharts.widgets';
	import GammelTheme from 'fusioncharts/themes/fusioncharts.theme.gammel';
	import CandyTheme from 'fusioncharts/themes/fusioncharts.theme.candy';
	// @ts-ignore
	import SvelteFC, { fcRoot } from 'svelte-fusioncharts';
	import { onMount } from 'svelte';

	// Always set FusionCharts as the first parameter
	$: fcRoot(FusionCharts, Widgets, darkMode ? CandyTheme : GammelTheme);

	//STEP 2 : preparing the chart Data
	export let title: string;
	export let subtitle: string = '';
	export let value: number;
	export let height = 250;
	export let width = 450;
	export let lowerLimit = 0;
	export let upperLimit = 100;
	export let showTickValues = true;
	export let targets: { value: number; name: string }[] = [];
	let colorStops: any;
	$: colorStops = [
		{
			minValue: `${lowerLimit}`,
			maxValue: `${lowerLimit + (upperLimit - lowerLimit) * 0.25}`,
			code: '#ffe6a7'
		},
		{
			minValue: `${lowerLimit + (upperLimit - lowerLimit) * 0.25}`,
			maxValue: `${lowerLimit + (upperLimit - lowerLimit) * 0.75}`,
			code: '#ffab54'
		},
		{
			minValue: `${lowerLimit + (upperLimit - lowerLimit) * 0.25}`,
			maxValue: `${lowerLimit + (upperLimit - lowerLimit)}`,
			code: '#F2726F'
		}
	];

	export let darkMode = false;
	let colorRange: any;
	$: colorRange = {
		color: colorStops
	};
	let dials: any;
	$: dials = {
		dial: [
			{
				value: `${value}`
			}
		]
	};
	//STEP 3: Create your configuration object
	let chartConfigs: any;
	$: chartConfigs = {
		type: 'angulargauge', // The gauge type
		width: width, // Width of the gauge
		height: height, // Height of the gauge
		dataFormat: 'json', // Data type
		renderAt: 'chart-container', //Container where the gauge will render
		dataSource: {
			// Gauge Configuration
			chart: {
				caption: title,
				subcaption: subtitle,
				lowerLimit: lowerLimit,
				upperLimit: upperLimit,
				showValue: '0',
				numberSuffix: '%',
				showTickValues: showTickValues,
				showToolTip: '0',
				theme: darkMode ? 'candy' : 'gammel',
				bgColor: darkMode ? '#111827' : '#FFFFFF'
			},
			// Chart Data
			colorRange: colorRange,
			dials: dials,
			trendpoints: {
				point: targets.map((t) => 
					({
						startvalue: t.value,
						displayvalue: t.name,
						thickness: '2',
						color: '#E15A26',
						usemarker: '1',
						markerbordercolor: '#E15A26',
						markertooltext: '80%'
					})
				)
			}
		}
	};
</script>

<div id="chart-container">
	<SvelteFC {...chartConfigs} />
</div>
