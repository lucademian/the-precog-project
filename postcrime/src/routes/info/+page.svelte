<script lang="ts">
	import AdvancedOptionsIcon from 'svelte-material-icons/Wrench.svelte';
	import MenuOpenIcon from 'svelte-material-icons/Menu.svelte';
	import MenuCloseIcon from 'svelte-material-icons/MenuOpen.svelte';
	import ArrowRightThick from 'svelte-material-icons/ArrowRightThick.svelte';
	import * as tf from '@tensorflow/tfjs';
	import { titleCase } from 'title-case';
	// @ts-ignore
	import groupBy from 'lodash.groupby';

	import GraphCard from './_components/GraphCard.svelte';

	import {
		Heading,
		WidgetPlaceholder,
		Drawer,
		Button,
		CloseButton,
		Label,
		NumberInput,
		DarkMode,
		Skeleton,
		Accordion,
		AccordionItem,
		Card
	} from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import MultiSelect from './_components/MultiSelect.svelte';
	import PlacesAutocompleteInput from './_components/PlacesAutocompleteInput.svelte';
	import MyFooter from '$lib/my_footer.svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import type {
		Tensor,
		TensorContainer,
		TensorContainerArray,
		TensorContainerObject
	} from '@tensorflow/tfjs';
	import Dial from './_components/graphs/Dial.svelte';
	import UsStates from './_components/graphs/USStates.svelte';

	let drawerHidden = false;
	let loading = true;
	let transitionParams = {
		x: -320,
		duration: 200,
		easing: sineIn
	};

	type DemographicInfo = {
		genders: { value: string; name: string }[];
		armed_options: { value: string; name: string }[];
		age: number;
		ethnicities: { value: string; name: string }[];
	};

	let shootingsData: tf.data.CSVDataset;
	let homicideData: tf.data.CSVDataset;
	let censusData: tf.data.CSVDataset;
	let calculateData: (
		shootingsData: tf.data.CSVDataset,
		homicideData: tf.data.CSVDataset,
		censusData: tf.data.CSVDataset,
		selected_armed: string[],
		selected_genders: string[],
		selected_ethnicities: string[],
		selected_states: string[],
		selected_age_range: string | undefined
	) => Promise<void> = async () => {};


	onMount(async () => {
		shootingsData = tf.data.csv('datasets/washingtonpost/shootings-data-augmented.csv');
		homicideData = tf.data.csv('datasets/washingtonpost/homicide-data-augmented.csv');
		censusData = tf.data.csv('datasets/uscensus/acs2015_census_tract_data_aggregated.csv');

		let stateAbbrevData = tf.data.csv('datasets/state_abbrev.csv');
		states = [
			{ value: 'a', name: 'Any' },
			...[
				...(await stateAbbrevData
					.map((row) => {
						return {
							// @ts-ignore
							value: row['Abbreviation'] as string,
							// @ts-ignore
							name: titleCase(row['State'])
						};
					})
					.toArray())
			]
		];

		armed_options = [
			{ value: 'a', name: 'Any' },
			...[
				...new Set(
					(
						await shootingsData
							.map((row) => {
								// @ts-ignore
								return row['armed_with']?.split(';');
							})
							.toArray()
					).flat()
				)
			]
				.filter((e) => e !== undefined)
				.map((e) => ({ value: e, name: titleCase(e.replace(/_/g, ' ')) }))
		];
		genders = [
			{ value: 'a', name: 'Any' },
			...[
				...new Set(
					(
						await shootingsData
							.map((row) => {
								// @ts-ignore
								return row['gender']?.split(';');
							})
							.toArray()
					).flat()
				)
			]
				.filter((e) => e !== undefined)
				.map((e) => ({ value: e, name: titleCase(e.replace(/_/g, ' ')) }))
		];

		let filterData = (
			data: any[],
			selected_armeds: string[],
			selected_genders: string[],
			selected_ethnicities: string[],
			selected_states: string[],
			selected_age_range: string | undefined
		) => {
			let filteredData = data
				// @ts-ignore
				.filter((row) => {
					// @ts-ignore
					return selected_genders.some((g) => g === 'a' || row['gender']?.split(';').includes(g));
				})
				// @ts-ignore
				.filter((row) => {
					// @ts-ignore
					return selected_ethnicities.some((g) => g === 'a' || row['race']?.split(';').includes(g));
				})
				// @ts-ignore
				.filter((row) => {
					return selected_armeds.some(
						// @ts-ignore
						(g) =>
							g === 'a' ||
							!Object.hasOwn(row, 'armed_with') ||
							row['armed_with']?.split(';').includes(g)
					);
				})
				// @ts-ignore
				.filter((row) => {
					return selected_states.some(
						// @ts-ignore
						(g) => g === 'a' || row['state'] === g
					);
				})
				// @ts-ignore
				.filter((row) => {
					return selected_age_range === undefined || row['age_range'] === selected_age_range;
				})
				// @ts-ignore
				.filter((row) => age <= 0 || (row['age'] > (age ?? 0) - 2 && row['age'] < (age ?? 0) + 2));
			return filteredData;
		};

		calculateData = async (
			shootingsData: tf.data.CSVDataset,

			homicideData: tf.data.CSVDataset,
			censusData: tf.data.CSVDataset,
			selected_armeds: string[],
			selected_genders: string[],
			selected_ethnicities: string[],
			selected_states: string[],
			selected_age_range: string | undefined
		) => {
			// load data from csv
			let shootingDataArr = await shootingsData.toArray();
			// @ts-ignore
			let homicideDataArr = (await homicideData.toArray()).filter((e) => e['state'] !== 'PR');
			let censusDataArr = await censusData.toArray();

			// filter rows
			let nShootingsInSelectedStates = filterData(
				shootingDataArr,
				['a'],
				['a'],
				['a'],
				selected_states,
				undefined
			).length;
			let nHomicidesInSelectedStates = filterData(
				homicideDataArr,
				['a'],
				['a'],
				['a'],
				selected_states,
				undefined
			).length;
			let filteredShootingsData = filterData(
				shootingDataArr,
				selected_armeds,
				selected_genders,
				selected_ethnicities,
				selected_states,
				selected_age_range
			);
			let filteredHomicidesData = filterData(
				homicideDataArr,
				selected_armeds,
				selected_genders,
				selected_ethnicities,
				selected_states,
				selected_age_range
			);

			// calculate base percentages
			percent_shootings = (100 * filteredShootingsData.length) / nShootingsInSelectedStates;
			percent_homicides = (100 * filteredHomicidesData.length) / nHomicidesInSelectedStates;

			// group data by state
			// @ts-ignore
			let stateShootingsRowMap = groupBy(shootingDataArr, (r) => r['state']);
			// @ts-ignore
			let stateHomicidesRowMap = groupBy(homicideDataArr, (r) => r['state']);
			// @ts-ignore
			let stateCensusRowMap = groupBy(censusDataArr, (r) => r['state']);

			// reset data fields
			states_shooting_percent_map_data = [];
			states_bodycam_data = [];
			states_shooting_percent_map_data_matching = [];
			states_homicide_percent_map_data = [];
			states_homicide_percent_map_data_matching = [];
			let prob_shooting_given_filter_temp = 0;
			let prob_homicide_given_filter_temp = 0;
			let selectedStatesPop = 0;
			let selectedStatesWithHomicidesPop = 0;
			let allStatesWithHomicidesTotal = 0;

			for (let state in stateShootingsRowMap) {
				if (!Object.hasOwn(stateHomicidesRowMap, state)) {
					stateHomicidesRowMap[state] = [];
				}

				let stateCensusData = stateCensusRowMap[state][0] as tf.TensorContainerObject;
				let stateIncluded = selected_states.includes('a') || selected_states.includes(state);
				states_shooting_percent_map_data.push({
					id: state,
					value: Math.round(
						(stateShootingsRowMap[state].length / nShootingsInSelectedStates) * 100
					),
					showLabel: true
				});

				states_homicide_percent_map_data.push({
					id: state,
					value: Math.round(
						(stateHomicidesRowMap[state].length / nHomicidesInSelectedStates) * 100
					),
					showLabel: true
				});

				let matchingShootingRows = filterData(
					stateShootingsRowMap[state],
					selected_armeds,
					selected_genders,
					selected_ethnicities,
					selected_states,
					selected_age_range
				);
				states_shooting_percent_map_data_matching.push({
					id: state,
					value: Math.round(
						(matchingShootingRows.length / stateShootingsRowMap[state].length) * 100
					),
					showLabel: true
				});

				let matchingHomicideRows = filterData(
					stateHomicidesRowMap[state],
					selected_armeds,
					selected_genders,
					selected_ethnicities,
					selected_states,
					selected_age_range
				);
				states_homicide_percent_map_data_matching.push({
					id: state,
					value: stateHomicidesRowMap[state].length == 0 ? null : Math.round(
						(matchingHomicideRows.length / stateHomicidesRowMap[state].length) * 100
					),
					showLabel: true
				});

				let bodycamCount = stateShootingsRowMap[state].filter(
					// @ts-ignore
					(r) => r['body_camera'] === 'True'
				).length;
				states_bodycam_data.push({
					id: state,
					value: Math.round((bodycamCount / stateShootingsRowMap[state].length) * 100),
					showLabel: true
				});

				if (stateIncluded) {
					// calculate givens for shootings
					let p_race_given_shoot =
						filterData(
							stateShootingsRowMap[state],
							['a'],
							['a'],
							selected_ethnicities,
							['a'],
							undefined
						).length / stateShootingsRowMap[state].length;
					let p_gender_given_shoot =
						filterData(
							stateShootingsRowMap[state],
							['a'],
							selected_genders,
							['a'],
							['a'],
							undefined
						).length / stateShootingsRowMap[state].length;
					let p_age_given_shoot =
						filterData(stateShootingsRowMap[state], ['a'], ['a'], ['a'], ['a'], selected_age_range)
							.length / stateShootingsRowMap[state].length;

					// calculate givens for homicides
					let p_race_given_homicide =
						filterData(
							stateHomicidesRowMap[state],
							['a'],
							['a'],
							selected_ethnicities,
							['a'],
							undefined
						).length / stateHomicidesRowMap[state].length;
					let p_gender_given_homicide =
						filterData(
							stateHomicidesRowMap[state],
							['a'],
							selected_genders,
							['a'],
							['a'],
							undefined
						).length / stateHomicidesRowMap[state].length;
					let p_age_given_homicide =
						filterData(stateHomicidesRowMap[state], ['a'], ['a'], ['a'], ['a'], selected_age_range)
							.length / stateHomicidesRowMap[state].length;
					// @ts-ignore
					let totalpop: number = stateCensusData['totalpop'];

					// priors for shootings and homicides
					let p_shoot = stateShootingsRowMap[state].length / totalpop;
					let p_homicide = stateHomicidesRowMap[state].length / totalpop;

					// demographic priors
					let p_age =
						selected_age_range !== undefined
							? (stateCensusData[`${selected_age_range}_ratio`] as number) / 100
							: 1;
					let p_race =
						selected_ethnicities.indexOf('a') > -1
							? 1
							: selected_ethnicities
									.filter((r) => Object.hasOwn(stateCensusData, r))
									.map((r) => stateCensusData[r] as number)
									.reduce((a, b) => a + b, 0) / 100;
					let p_gender =
						selected_genders.indexOf('a') > -1
							? 1
							: selected_genders
									.filter((r) => Object.hasOwn(stateCensusData, r))
									.map((r) => stateCensusData[r] as number)
									.reduce((a, b) => a + b, 0) / 100;

					// calculate probabilities using bayes for shootings
					let p_shoot_given_race =
						Math.log(p_race_given_shoot) + Math.log(p_shoot) - Math.log(p_race);
					let p_shoot_given_gender =
						Math.log(p_gender_given_shoot) + Math.log(p_shoot) - Math.log(p_gender);
					let p_shoot_given_age = Math.log(p_age_given_shoot) + Math.log(p_shoot) - Math.log(p_age);
					let prob_shoot_given_filter =
						p_shoot_given_race + p_shoot_given_gender + 0 - Math.log(p_shoot);

					// calculate probabilities using bayes for homicides
					let p_homicide_given_race =
						Math.log(p_race_given_homicide) + Math.log(p_homicide) - Math.log(p_race);
					let p_homicide_given_gender =
						Math.log(p_gender_given_homicide) + Math.log(p_homicide) - Math.log(p_gender);
					let p_homicide_given_age =
						Math.log(p_age_given_homicide) + Math.log(p_homicide) - Math.log(p_age);
					let prob_homicide_given_filter =
						p_homicide_given_race + p_homicide_given_gender + 0 - Math.log(p_homicide);

					prob_shooting_given_filter_temp += Math.exp(prob_shoot_given_filter + Math.log(totalpop));

					if (!isNaN(prob_homicide_given_filter)) {
						prob_homicide_given_filter_temp += Math.exp(
							prob_homicide_given_filter + Math.log(totalpop)
						);
						selectedStatesWithHomicidesPop += totalpop;
						allStatesWithHomicidesTotal += stateHomicidesRowMap[state].length;
					}
					selectedStatesPop += totalpop;
				}
			}

			// take weighted average of probabilities
			prob_shooting_given_filter = Math.exp(
				Math.log(prob_shooting_given_filter_temp) - Math.log(selectedStatesPop) + Math.log(100)
			);
			prob_homicide_given_filter = Math.exp(
				Math.log(prob_homicide_given_filter_temp) -
					Math.log(selectedStatesWithHomicidesPop) +
					Math.log(100)
			);

			let statesFiltered = !selected_states.includes('a');

			// get prior probabilities without filter
			let priorShootingProb = (100 * nShootingsInSelectedStates) / selectedStatesPop;
			let priorHomicideProb = (100 * allStatesWithHomicidesTotal) / selectedStatesWithHomicidesPop;

			// set data for charts
			prob_shooting_targets = [
				{ value: priorShootingProb, name: statesFiltered ? 'In Selected States' : 'Nationwide' }
			];
			prob_homicide_targets = [
				{ value: priorHomicideProb, name: statesFiltered ? 'In Selected States' : 'Nationwide' }
			];

			prob_shooting_upper_limit = Math.max(
				priorShootingProb / 0.625,
				prob_shooting_given_filter / 0.9
			);
			prob_homicide_upper_limit = Math.max(
				priorHomicideProb / 0.625,
				prob_homicide_given_filter / 0.9
			);

			prob_shooting_subtitle = `Your Prob: ${Math.round(
				prob_shooting_given_filter * 10000
			)} / 10,000; &nbsp;&nbsp; Avg. Prob: ${Math.round(priorShootingProb * 10000)} / 10,000`;
			prob_homicide_subtitle = `Your Prob: ${Math.round(
				prob_homicide_given_filter * 10000
			)} / 10,000; &nbsp;&nbsp; Avg. Prob: ${Math.round(priorHomicideProb * 10000)} / 10,000`;
		};

		loading = false;
	});

	$: calculateData(
		shootingsData,
		homicideData,
		censusData,
		selected_armeds,
		selected_genders,
		selected_ethnicities,
		selected_states,
		age_range
	);

	// fields for police shootings map displays
	let states_shooting_percent_map_data: { id: string; value: number; showLabel: boolean }[];
	let states_shooting_percent_map_data_matching: {
		id: string;
		value: number;
		showLabel: boolean;
	}[];
	let states_bodycam_data: { id: string; value: number; showLabel: boolean }[];
	states_bodycam_data = [];
	states_shooting_percent_map_data = [];
	states_shooting_percent_map_data_matching = [];

	// fields for homicides map displays
	let states_homicide_percent_map_data: { id: string; value: number | null; showLabel: boolean }[];
	let states_homicide_percent_map_data_matching: {
		id: string;
		value: number | null;
		showLabel: boolean;
	}[];
	states_homicide_percent_map_data = [];
	states_homicide_percent_map_data_matching = [];

	// fields for percent shootings matching display
	let percent_shootings = 0;

	// fields for percent homicides matching display
	let percent_homicides = 0;

	// fields for probability of police shooting display
	let prob_shooting_given_filter = 0;
	let prob_shooting_targets: { name: string; value: number }[] = [];
	let prob_shooting_upper_limit = 0.01;
	let prob_shooting_subtitle = '';

	// fields for probability of homicide display
	let prob_homicide_given_filter = 0;
	let prob_homicide_targets: { name: string; value: number }[] = [];
	let prob_homicide_upper_limit = 0.01;
	let prob_homicide_subtitle = '';

	let age: number | undefined;
	let age_range: string | undefined;

	let ageToRange: (age: number | undefined) => string | undefined = (age) => {
		if (age == undefined || age <= 0) {
			return undefined;
		} else if (age < 19) {
			return '0-18';
		} else if (age < 26) {
			return '19-25';
		} else if (age < 35) {
			return '26-34';
		} else if (age < 55) {
			return '35-54';
		} else if (age < 65) {
			return '55-64';
		} else {
			return '65+';
		}
	};
	$: age_range = ageToRange(age);

	let selected_genders = ['a'];
	let genders = [{ value: 'a', name: 'Any' }];

	let selected_ethnicities = ['a'];
	let ethnicities = [
		{ value: 'a', name: 'Any' },
		{ value: 'W', name: 'White' },
		{ value: 'B', name: 'Black' },
		{ value: 'A', name: 'Asian heritage' },
		{ value: 'N', name: 'Native American' },
		{ value: 'H', name: 'Hispanic' },
		{ value: 'O', name: 'Other' },
		{ value: 'U', name: 'Unknown' }
	];

	let selected_armeds = ['a'];
	let armed_options = [{ value: 'a', name: 'Any' }];

	let selected_states = ['a'];
	let states = [{ value: 'a', name: 'Any' }];

	let darkMode = false;
	$: darkMode = localStorage.getItem('color-theme') === 'dark';

</script>

<div id="page">
	<!-- Sidebar -->
	<Drawer
		activateClickOutside={false}
		transitionType="fly"
		backdrop={false}
		{transitionParams}
		bind:hidden={drawerHidden}
		id="sidebar"
	>
		<div class="flex flex-col h-full">
			<div class="flex-grow overflow-y-auto px-4 box-border mt-7">
				<Label
					>Gender
					<MultiSelect
						bind:selectedValues={selected_genders}
						options={genders}
						mutuallyExclusiveValue="a"
					/>
				</Label>
				<Label class="pt-4"
					>Ethnicity
					<MultiSelect
						bind:selectedValues={selected_ethnicities}
						options={ethnicities}
						mutuallyExclusiveValue="a"
					/>
				</Label>
				<Label class="pt-4"
					>Age
					<NumberInput class="mt-2" bind:value={age} />
				</Label>
				<Label class="pt-4 mb-6"
					>State
					<MultiSelect
						bind:selectedValues={selected_states}
						options={states}
						mutuallyExclusiveValue="a"
					/>
				</Label>

				<Accordion
					activeClasses="bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-500"
				>
					<AccordionItem>
						<span slot="header"
							><AdvancedOptionsIcon class="inline-block mr-4" />Advanced Options</span
						>

						<Label class="pt-4"
							>Suspect Weapon
							<MultiSelect
								bind:selectedValues={selected_armeds}
								options={armed_options}
								mutuallyExclusiveValue="a"
							/>
						</Label>
					</AccordionItem>
				</Accordion>
				<div class="pt-8">
					<Button on:click={() => (drawerHidden = true)}
						>See Results<ArrowRightThick class="ml-2" /></Button
					>
				</div>
			</div>
		</div>
	</Drawer>

	<div
		class="flex flex-col fixed w-screen h-screen box-border {!drawerHidden
			? 'pl-80'
			: ''} transition-all"
	>
		<!-- Top Bar -->
		<div
			class="p-5 top-0 left-0 right-0 border-gray-300 dark:border-gray-700 border-b bg-white dark:bg-gray-900 z-10"
		>
			<div class="inline-block align-middle">
				<Button
					pill={true}
					outline={true}
					on:click={() => (drawerHidden = !drawerHidden)}
					class="inline-block p-0"
				>
					{#if drawerHidden}
						<MenuOpenIcon size="24" />
					{:else}
						<MenuCloseIcon size="24" />
					{/if}
				</Button>
			</div>
			<h5 class="inline-block text-2xl ml-5 align-middle">
				<a href="/"
					><span
						class="from-blue-400 to-blue-800 dark:from-blue-100 dark:to-blue-400 text-transparent bg-clip-text bg-gradient-to-br font-black font-mono"
					>
						The Precog Project
					</span></a
				>
			</h5>
			<DarkMode class="block ml-5 float-right" />
		</div>

		<!-- Contents -->
		<div class="flex-grow p-10 box-border overflow-y-auto flex flex-wrap flex-row">
			<!-- Spedometers for homicides -->
			<GraphCard bind:loading width={400} height={300}>
				<Dial
					width={390 - 8}
					height={300 - 8}
					bind:darkMode
					bind:value={percent_homicides}
					title="Percent of Homicides Involving Victims Matching Your Profile in Selected States"
				/>
			</GraphCard>
			<GraphCard bind:loading width={400} height={300}>
				<Dial
					width={390 - 8}
					height={300 - 8}
					bind:upperLimit={prob_homicide_upper_limit}
					bind:darkMode
					bind:targets={prob_homicide_targets}
					bind:value={prob_homicide_given_filter}
					bind:subtitle={prob_homicide_subtitle}
					showTickValues={false}
					title="Probability You Would Be a Victim of a Homicide Given Your Profile"
				/>
			</GraphCard>

			<!-- Spedometers for police shootings -->
			<GraphCard bind:loading width={400} height={300}>
				<Dial
					width={390 - 8}
					height={300 - 8}
					bind:darkMode
					bind:value={percent_shootings}
					title="Percent of Fatal Police Shootings Involving Victims Matching Your Profile in Selected States"
				/>
			</GraphCard>
			<GraphCard bind:loading width={400} height={300}>
				<Dial
					width={390 - 8}
					height={300 - 8}
					bind:upperLimit={prob_shooting_upper_limit}
					bind:darkMode
					bind:targets={prob_shooting_targets}
					bind:value={prob_shooting_given_filter}
					bind:subtitle={prob_shooting_subtitle}
					showTickValues={false}
					title="Probability You Would Be a Victim of a Fatal Police Shooting Given Your Profile"
				/>
			</GraphCard>

			<!-- Homicide Map displays -->
			<GraphCard bind:loading width={800} height={600}>
				<UsStates
					width={800 - 8}
					height={600 - 8}
					bind:darkMode
					title="Percent of Homicides with Victims Matching Your Profile per State"
					bind:mapData={states_homicide_percent_map_data_matching}
					numberSuffix="%"
				/>
			</GraphCard>
			<GraphCard bind:loading width={800} height={600}>
				<UsStates
					width={800 - 8}
					height={600 - 8}
					bind:darkMode
					title="Percent of Homicides per State"
					bind:mapData={states_homicide_percent_map_data}
					numberSuffix="%"
				/>
			</GraphCard>

			<!-- Shootings map displays -->
			<GraphCard bind:loading width={800} height={600}>
				<UsStates
					width={800 - 8}
					height={600 - 8}
					bind:darkMode
					title="Percent of Fatal Police Shootings with Victims Matching Your Profile per State"
					bind:mapData={states_shooting_percent_map_data_matching}
					numberSuffix="%"
				/>
			</GraphCard>
			<GraphCard bind:loading width={800} height={600}>
				<UsStates
					width={800 - 8}
					height={600 - 8}
					bind:darkMode
					title="Percent of Fatal Police Shootings per State"
					bind:mapData={states_shooting_percent_map_data}
					numberSuffix="%"
				/>
			</GraphCard>
			<GraphCard bind:loading width={800} height={600}>
				<UsStates
					width={800 - 8}
					height={600 - 8}
					bind:darkMode
					title="Body Camera Usage Rate in Fatal Police Shootings By State"
					bind:mapData={states_bodycam_data}
					numberSuffix="%"
				/>
			</GraphCard>
			<MyFooter className="h-min mt-20 mx-5 w-full" />
		</div>
	</div>
</div>

<style></style>
