<script>
	import ArrowRightThick from 'svelte-material-icons/ArrowRightThick.svelte';
	import MyFooter from '$lib/my_footer.svelte';
	import {
		Button,
		P,
		Footer,
		FooterLink,
		FooterLinkGroup,
		FooterCopyright,
		DarkMode,
		Navbar,
		NavBrand,
		Span,
		Heading
	} from 'flowbite-svelte';
</script>

<div id="page" class="w-screen overflow-x-hidden">
	<div class="max-w-2xl mx-auto mt-20">
		<Navbar navClass="px-0 py-2.5"
			><NavBrand
				><Heading tag="h1" class="mb-4 ml-0" customSize="text-2xl md:text-3xl lg:text-4xl"
					><h1
						class="pb-2 from-blue-400 to-blue-800 dark:from-blue-100 dark:to-blue-400 text-transparent bg-clip-text bg-gradient-to-br font-black font-mono"
					>
						The Precog Project
					</h1></Heading
				></NavBrand
			><DarkMode /></Navbar
		>
		<div class="mb-6 block">
			<Heading tag="h2" class="mb-4 ml-0" customSize="text-xl md:text-xl lg:text-2xl"
				><h2
					class="pb-2 from-blue-400 to-blue-800 dark:from-blue-100 dark:to-blue-400 text-transparent bg-clip-text bg-gradient-to-br font-black font-mono"
				>
					What is the Precog Project?
				</h2></Heading
			>
			<P class="" color="text-gray-500 dark:text-gray-400"
				>We first did exploratory data analysis on the datasets gathered, those being from
				Washington Post and US Census datasets. This allowed us to clean the data, and we could then
				calculate the probabilities of homicide based on gender, age, race, and location, as well as
				the likelihood of someone being affected by a police shooting (based on the same factors).
				This was done by creating a probability function that found the conditional probability of
				an incident given a set of attributes all of this aformentioned data science work was done
				in Python. This logic was then ported over to a JavaScript/svelte front-end that represents
				all this data and allows the users of the website to find out where they fall under
				according to their demographics and our calculated probabilities.
			</P>

			<Button class="w-full max-w-md block mt-3" href="info"
				>Get Started <ArrowRightThick class="icon ml-4" /></Button
			>

			<Heading tag="h2" class="mb-4 mt-6 ml-0" customSize="text-xl md:text-xl lg:text-2xl"
				><h2
					class="pb-2 from-blue-400 to-blue-800 dark:from-blue-100 dark:to-blue-400 text-transparent bg-clip-text bg-gradient-to-br font-black font-mono"
				>
					Datasets Used
				</h2></Heading
			>
			<Heading tag="h3" class="mb-2 mt-4 ml-0" customSize="text-lg"
				><h3
					class="pb-2 from-blue-400 to-blue-800 dark:from-blue-100 dark:to-blue-400 text-transparent bg-clip-text bg-gradient-to-br font-black font-mono"
				>
				The Washington Post Police Shooting Dataset
				</h3></Heading
			>
			<P class="" color="text-gray-500 dark:text-gray-400">
				The Washington Post Police shooting dataset contains records of all persons shot by an on-duty police officer from 2015 to 2023, in the
				United States, as well as the agencies involved in each event. It is updated regularly as
				fatal shootings are reported and as facts emerge about individual cases. The Washington Post
				Homicide Dataset: The Washington Post collected data on more than 52,000 criminal homicides
				over the past 10 years in 50 of the largest American cities. The data included the location
				of the homicide, whether an arrest occurred and, demographic information about the victim.
			</P>
			<Heading tag="h3" class="mb-2 mt-4 ml-0" customSize="text-lg"
				><h3
					class="pb-2 from-blue-400 to-blue-800 dark:from-blue-100 dark:to-blue-400 text-transparent bg-clip-text bg-gradient-to-br font-black font-mono"
				>
				2020 US Census Dataset (from Kaggle)
				</h3></Heading
			>
			<P class="" color="text-gray-500 dark:text-gray-400">

				This dataset is from the US Census website and was
				cleaned for Kaggle to increase accessibility. There are no personal identifiable information
				in this dataset.
			</P>

			<Heading tag="h3" class="mb-2 mt-4 ml-0" customSize="text-lg"
				><h3
					class="pb-2 from-blue-400 to-blue-800 dark:from-blue-100 dark:to-blue-400 text-transparent bg-clip-text bg-gradient-to-br font-black font-mono"
				>
				US 2021 Age Distribution Dataset
				</h3></Heading
			>
				<P class="" color="text-gray-500 dark:text-gray-400 pb-10">
				Population and demographic data in this
				dataset is based on analysis of the Census Bureau's American Community Survey (ACS) and thus
				it may differ from other population estimates by the Census Bureau. The US and state
				population data displayed on this site are only for civilians. Population numbers are
				rounded to the nearest 100.
			</P>
		</div>
	</div>
	<MyFooter className="" />
</div>
