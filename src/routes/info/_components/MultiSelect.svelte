<script lang="ts">
	import { Button, Checkbox, Chevron, Dropdown } from 'flowbite-svelte';
	import { onMount } from 'svelte';

	type SelectOption = {
		value: string;
		name: string;
	};

	export let options: SelectOption[] = [];
	export let mutuallyExclusiveValue: string | null = null;
	export let selectedValues: string[];

	let checkedBools: boolean[] = [];
	let mutuallyExclusiveIdx = -1;

	checkedBools = options.map((o) => selectedValues.includes(o.value));

	$: {
		mutuallyExclusiveIdx = options.findIndex((o) => o.value == mutuallyExclusiveValue);
	}

	$: {
		selectedValues = checkedBools
			.map((e, i) => (e ? options[i].value : null))
			.filter((e) => e != null) as string[];
	}
</script>

<Button color="light" class="block w-full text-sm p-2.5 mt-2"
	><Chevron placement="bottom-end"
		><div class="w-full text-left">
			{#if selectedValues.length == 0}
				Please Select
			{:else}
				{#each selectedValues as value, i}
					{(i > 0 ? ', ' : '') + options.find((e) => e.value == value)?.name}
				{/each}
			{/if}
		</div></Chevron
	></Button
>
<Dropdown class="overflow-y-auto px-3 pb-3 text-sm">
	{#each options as option, i}
		<li class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600">
			<Checkbox
				on:change={mutuallyExclusiveValue === null
					? null
					: option.value == mutuallyExclusiveValue
					? (c) => {
							checkedBools = checkedBools.fill(false);
							if (mutuallyExclusiveIdx > -1) {
								checkedBools[mutuallyExclusiveIdx] = true;
							}
					  }
					: (c) =>
							checkedBools[i]
								? (checkedBools[mutuallyExclusiveIdx] = false)
								: !checkedBools.some((e) => e)
								? (checkedBools[mutuallyExclusiveIdx] = true)
								: null}
				bind:checked={checkedBools[i]}>{option.name}</Checkbox
			>
		</li>
	{/each}
</Dropdown>
