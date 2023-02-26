<script lang="ts">
	import FusionCharts from 'fusioncharts';
	import Maps from 'fusioncharts/fusioncharts.maps';
	import Usa from 'fusioncharts/maps/fusioncharts.usa';
	import GammelTheme from 'fusioncharts/themes/fusioncharts.theme.gammel';
	import CandyTheme from 'fusioncharts/themes/fusioncharts.theme.candy';
	// @ts-ignore
	import SvelteFC, { fcRoot } from 'svelte-fusioncharts';

	export let darkMode = false;
	fcRoot(FusionCharts, Maps, Usa, darkMode ? CandyTheme : GammelTheme);

	//STEP 2 : Preparing the map Data
	export let mapData: { id: string; value: number | null; showLabel: boolean }[];
	export let width: number = 400;
	export let height: number = 200;

	export let title: string,
		subtitle: string = '',
		numberSuffix: string = '';

	let maxVal: number, minVal: number;
    $: maxVal = mapData.filter((d) => d !== null).map((d) => d.value).reduce((a, b) => Math.max(a!, b!), 0) as number;
	$: minVal = mapData.filter((d) => d !== null).map((d) => d.value).reduce((a, b) => Math.min(a!, b!), 0) as number;

	//STEP 3: Create your chart configuration
	let colorRange: any;
    $: colorRange = {
		minvalue: '0',
		code: '#FFE0B2',
		gradient: '1',
		color: [
			{
				minvalue: minVal,
				maxvalue: maxVal / 2,
				color: '#FFD74D'
			},
			{
				minvalue: maxVal / 2,
				maxvalue: maxVal,
				color: '#DC3A21'
			}
		]
	};

	let mapConfigs: any;
    $: mapConfigs = {
		type: 'usa', // Map type
		width: width, // Width of the chart
		height: height, // Height of the chart
		dataFormat: 'json', // Data Type
		renderAt: 'chart-container', //container where the chart will render
		dataSource: {
			// Map Configuration
			chart: {
				caption: title,
				subcaption: subtitle,
				numbersuffix: numberSuffix,
				includevalueinlabels: '1',
				labelsepchar: ': ',
				entityFillHoverColor: '#FFF9C4',
				theme: darkMode ? 'candy' : 'gammel',
				bgColor: darkMode ? '#111827' : '#FFFFFF',
                showBorder: '1',
                // baseFontColor: darkMode ? '#FFFFFF' : '#000000',
			},
			// Aesthetics; ranges synced with the slider
			colorrange: colorRange,
			// Source data as JSON --> id represents continents of the world.
			data: mapData
		}
	};
</script>

<div id="chart-container">
	<SvelteFC {...mapConfigs} />
</div>
