<script>

	import { Footer, FooterCopyright, FooterLink, FooterLinkGroup } from "flowbite-svelte";
    export let className = '';
</script>
<Footer class={className}>
    <FooterCopyright
        href="#"
        by="Andre Kirby, Jake Friedman, Luca Demian, and Nicolai Jacobsen"
        year={2023}
    />
    <FooterLinkGroup
        ulClass="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0 ml-20"
    >
        <!-- <FooterLink href="/about">About & Contact</FooterLink>
        <FooterLink href="/privacy">Privacy Policy</FooterLink>
        <FooterLink href="/licenses">Licenses</FooterLink>
        <FooterLink href="/sources">Data Sources</FooterLink> -->
    </FooterLinkGroup>
</Footer>