<script lang="ts">
	import { Skeleton } from "flowbite-svelte";
    export let loading = true;
    export let width: number | undefined = undefined, height: number | undefined = undefined;
    let style: string = '';
    $: {
        style = '';
        if (width !== undefined && width > 0) {
            style = `width: ${width}px !important;`;
        }
        if (height !== undefined && height > 0) {
            style = `${style} height: ${height}px !important;`;
        }
    }

</script>

<div class="m-2 p-1 border-gray-300 dark:border-gray-700 border h-min rounded-md" style={style}>
    {#if loading}
        <Skeleton />
    {/if}
    {#if !loading}
        <slot/>
    {/if}
</div>