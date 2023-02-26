
<svelte:head>
    <script async defer src='https://maps.googleapis.com/maps/api/js?key=AIzaSyDXWnji_rlO3y3wcbsRE4L5AyLGAK4iIVU&libraries=places'></script>
</svelte:head>

<script lang="ts">
    // @ts-ignore
    import AutoComplete from "simple-svelte-autocomplete";
	import { onMount } from "svelte";

    // const PUBLIC_GOOGLE_MAPS_KEY = "AIzaSyDXWnji_rlO3y3wcbsRE4L5AyLGAK4iIVU";
    // const loader = new Loader(
	// 	PUBLIC_GOOGLE_MAPS_KEY
	// );

     export let value: string = '';

    
    let mapsApiReady = false;
	onMount(() => {
		mapsApiReady = true;
	});


    async function getItems(searchText: string) {
        if (!mapsApiReady) {
            return [];
        }

        const service = new google.maps.places.AutocompleteService();
        const request = {
            input: searchText,
            types: ["(cities)"],
        };

        return new Promise((resolve, reject) => {
            service.getPlacePredictions(request, (results, status) => {
                if (status != google.maps.places.PlacesServiceStatus.OK) {
                    reject(status);
                } else {
                    resolve(results);
                }
            });
        });
    }

</script>

<div class="h-min">
    <AutoComplete
    searchFunction="{getItems}"
    delay="200"
    localFiltering={false}
    labelFieldName="description"
    valueFieldName="place_id"
    hideArrow={true}
    className='w-full'
    inputClassName='block w-full disabled:cursor-not-allowed disabled:opacity-50 focus:border-blue-500 focus:ring-blue-500 dark:focus:border-blue-500 dark:focus:ring-blue-500 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border-gray-300 dark:border-gray-600 p-2.5 text-sm rounded-lg mt-2'
    noInputStyles={true}
    bind:selectedItem="{value}"
    />
</div>