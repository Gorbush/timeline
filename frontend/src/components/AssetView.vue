/*
 * Copyright (C) 2021, 2022 Tobias Himstedt
 * 
 * 
 * This file is part of Timeline.
 * 
 * Timeline is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * Timeline is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 */
 
<template>
    <v-container ref="wall" fluid class="fill-height">
        <v-row class="fill-height">
            <v-col class="noscroll ma-2">
                <tile v-if="asset"
                :target-height="previewHeight" 
                @set-rating="setRating"
                @click-photo="clickPhoto"
                :asset="asset">
            </tile>                    

            </v-col>
            
            <div class="noscroll timelineContainer ma-2" 
                ref="timelineContainer"
                v-on:mousemove="calcPosition($event)"
                v-on:mouseenter="scrubbing = true"
                v-on:mouseleave="scrubbing = false"
                v-on:click="jumpToDate()">
                <div v-for="(tick, index) in ticks" :key="index" 
                    :style="{top:tick.pos + 'px',height:tick.height + 'px', position:'absolute', width:'30px'}" >
                    <div style="position: relative">
                        <tick :moment="tick.date" :h="tick.height"></tick>
                    </div>
                </div>
                <div id="tick" :style="cssProps"></div>
                <div v-if="scrubbing" id="currentDate" class="rounded-pill text-center" :style="cssProps">{{currDate}}</div>
            </div>
        
        </v-row>
        
        <v-dialog
            v-model="photoFullscreen"
            fullscreen hide-overlay
            @keydown="keyboardActionDialog($event)"
            ref="viewerDialog">
            <image-viewer :photo="asset" ref="viewer"
                            v-if="photoFullscreen && asset"
                            @close="closeViewer"
                            @set-rating="setRating"
                            @left="navigate(-1)"
                            @right="navigate(1)">
            </image-viewer>
        </v-dialog>
        
    </v-container>
 </template>

<script>
    import axios from "axios";
    import ImageViewer from "./ImageViewer";
    import Tick from "./Tick";
    import Tile from "./Tile.vue"
    import { mapState } from 'vuex'

    // const logBase = (n, base) => Math.log(n) / Math.log(base);
    
    export default {
        name: "AssetView",

        components: {
            ImageViewer,
            Tick,
            Tile
        },

        props: {
            personId: Number,
            assetId: Number,
            thingId: String,
            city: String,
            county: String,
            country: String,
            state: String,
            from: String,
            to: String,
            rating: Number,
            camera: String,
            albumId: Number,
            showPhotoCount: {
                type: Boolean,
                default: true
            },
            selectionAllowed: {
                type: Boolean,
                default: true
            }
        },
        data() { 
            return {
                photoFullscreen: false,
                asset: null,
                // ---
                min_date: null,
                max_date: null,
                total_scale: null,
                currentTick: 0,
                lastTickYPos: 0,
                currentTickYPos: 0,
                currDate: "",
                scrubbing: false,
                tickDates: [],
                totalAssets: 0,
                prevPhoto: null,
                nextPhoto: null,
                imageViewerDirection: 0,
                selectMulti: false,
                ticks: [],
            };
        },

        mounted() {
            this.$emit("set-goback", null);
            this.$store.commit("setSelectionAllowed", false);
            this.lastTickYPos = Number.MAX_VALUE;
            axios.get(`/api/asset/data/${this.assetId}`).then((result) => {
                this.asset = result.data;
            });
        },

        watch: {
        },

        computed: {

            ...mapState({
                previewHeight: state => state.person.previewHeight,
                selectedPhotos: state => state.photo.selectedPhotos
                
            }),
            cssProps() {
                return {
                    '--current-tick': this.currentTick + "px",
                    '--current-tick-text': (this.currentTick - 10) + 'px',
                    '--tick-color': this.$vuetify.theme.secondary
                }
            },
        },

         // eslint-disable-next-line no-unused-vars
        beforeRouteLeave(to, from, next) {
            this.$store.commit("emptySelectedPhotos");
            next();
        },

        methods: {
            
            closeViewer() {
                this.photoFullscreen = false;
                this.asset = null;
            },

            scrub(v) {
                this.scrubbing = v;
            },


            clickPhoto() {
                this.photoFullscreen = true;
                this.imageViewerDirection = 0;
            },

            setRating(value) {
                if (value <= 5 && this.asset) {
                    this.asset.setRating(value); 
                     if (this.photoFullscreen) 
                         this.$refs.viewer.mouseMove();
                           
                }
            },

            keyboardActionWall(event) {
                // are these values somewhere defined as constants?
            
                if (event.code == "Escape") {
                    this.photoFullscreen = false;
                    this.clearSelection();
                } else if (event.code.startsWith("Digit")) {
                    let value = parseInt(event.key);
                    this.setRating(value); 
                }
            },


            keyboardActionDialog(event) {
                // are these values somewhere defined as constants?
                if (event.code == "ArrowLeft")
                    this.navigate(-1);
                else if (event.code == "ArrowRight")
                    this.navigate(1);
                else if (event.code.startsWith("Digit")) {
                    let value = parseInt(event.key);
                    this.setRating(value);
                }
            },

            height(section) {
                const unwrappedWidth = (3 / 2) * section.num_assets * this.previewHeight * (7 / 10);
                const rows = Math.ceil(unwrappedWidth / this.$refs.wall.clientWidth);
                const height = rows * this.previewHeight;
                return height;
            },

        }
    }
</script>

<style scoped>

    .inscroll {
        overflow: scroll;

    }
    .scroller {
        position: absolute;
        top: 0px;
        bottom: 0px;
        left: 0px;
        right: 0px;
        overflow: scroll;
        /* IE and Edge */
        /*
        -ms-overflow-style: none;  
        */
        /* Firefox */
        /*
        scrollbar-width: none;
        */  
    }
    .scroller::-webkit-scrollbar {
        display: none;
    }

    .scroller:focus {
        outline-width: 0;
    }

    .tl {
        background-color: green;
        position: absolute;
        top: 0px;
        height: 100%;
        width: 60px;
        right: 0px;
    }

    .noscroll {
        position: relative;
    }

    .timelineContainer {
        width: 30px;
    }

    #tick {
        position: absolute;
        top: var(--current-tick);
        background-color:var(--v-primary-base);
        width:20px;
        height:2px;
        left: 10px;
    }

    #currentDate {
        position: absolute;
        top: var(--current-tick-text);
        width: 80px;
        color: black;
        background-color:var(--v-info-darken1);
        color: var(--v-info-lighten5);
        transform: translate(-90px, 0px);
    }

</style>
