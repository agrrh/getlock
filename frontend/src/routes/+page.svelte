<script>
	import { onMount } from 'svelte';
	import { invalidateAll } from '$app/navigation';

	export let data;

	onMount(() => {
		const interval = setInterval(() => {
			invalidateAll();
		}, 1000);

		return () => {
			clearInterval(interval);
		};
	});
</script>

<h1>Demo</h1>

{#if data.namespace}
	<h2>namespace/{data.namespace.id}</h2>
	{#each data.namespace.locks as lock}
		<div
			class="{lock.expired ? 'expired' : 'alive'}"
		>
			<h3>{lock.id}</h3>
			<p>
				🔑 {lock.uuid}
			</p>
			<p>
				🔖 {lock.timestamp}
				⏰ {lock.ttl}s
				{#if lock.age < lock.ttl}
					({lock.ttl - lock.age}s left)
				{/if}
			</p>
		</div>
	{/each}

{:else}
	<p>
		Loading ...
	</p>
{/if}

<style>
div {
	font-family: monospace;
	padding: 4pt 16pt;
}

div.expired {
	background-color: #eee;
}

div.alive {
	background-color: #eff;
}
</style>
