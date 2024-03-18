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
            <v-col class="noscroll ma-2" fill-height>
                <v-row fill-height>
                    <v-col class="noscroll ma-2" fill-height>
                        <tile v-if="asset"
                            :target-height="previewHeight" 
                            @set-rating="setRating"
                            @click-photo="clickPhoto"
                            :asset="asset">
                            </tile>                    
                    </v-col>
                </v-row>
                <v-row >
                    <v-col class="scroll ma-2">
                        <v-expand-x-transition>
                            <v-card light style="position:relative; width:360px; min-height:100vh" v-show="asset">
                                <div class="scroller" v-if="asset">
                                    <v-card>
                                        <v-card-title>
                                            Information
                                        </v-card-title>
            
                                        <div>
                                            <v-card-text>
                                                Text 01
                                            </v-card-text>
                                        </div>
                                        <div>
                                            <v-card-text>
                                                <div class="font-weight-bold">Details
                                                    <a :href="assetUrl(asset)">
                                                        <v-btn icon @click="clickAsset(asset.id)" v-if="asset.id">
                                                            <v-icon>mdi-open-in-app</v-icon>
                                                        </v-btn>
                                                    </a>
                                                </div>
                                            <v-list-item two-line>
                                                <v-list-item-avatar>
                                                    <v-icon>mdi-calendar</v-icon>
                                                </v-list-item-avatar>
                                                <v-list-item-content>
                                                    <v-list-item-title v-html="date(asset.created)"></v-list-item-title>
                                                    <v-list-item-subtitle v-html="time(asset.created)"></v-list-item-subtitle>
                                                </v-list-item-content>
                                            </v-list-item>
                                            <v-list-item two-line>
                                                <v-list-item-avatar>
                                                    <v-icon>mdi-folder</v-icon>
                                                </v-list-item-avatar>
                                                <v-list-item-content class="d-flex text-wrap">
                                                    {{asset.directory}}
                                                </v-list-item-content>
                                            </v-list-item>
                                            <!-- repair this; information is also available for Videos but not as exif -->
                                            <v-list-item two-line v-if="isPhoto">
                                                <v-list-item-avatar>
                                                    <v-icon>mdi-camera</v-icon>
                                                </v-list-item-avatar>
                                                <v-list-item-content>
                                                    <v-list-item-title v-html="asset.filename"></v-list-item-title>
                                                    <v-list-item-subtitle v-if="exif.ExifImageWidth && exif.ExifImageHeight">
                                                        <span class="exif-detail">{{size.toFixed(1)}} MP</span>
                                                        <span class="exif-detail">{{exif.ExifImageWidth}} x {{exif.ExifImageHeight}}</span>
                                                    </v-list-item-subtitle>
                                                </v-list-item-content>            
                                            </v-list-item>
                                            <v-list-item three-line v-if=isPhoto>
                                                <v-list-item-avatar>
                                                    <v-icon>mdi-camera-iris</v-icon>
                                                </v-list-item-avatar>
                                                <v-list-item-content>
                                                    <v-list-item-title>{{exif.Make}} {{exif.Model}}</v-list-item-title>
                                                    <v-list-item-subtitle>
                                                        <span class="exif-detail" v-if="exif.FNumber">f/{{exif.FNumber}}</span>  
                                                        <span class="exif-detail" v-if="exif.ExposureTime">{{exif.ExposureTime}}s</span>
                                                        <span class="exif-detail" v-if="exif.FocalLength">{{exif.FocalLength}} mm</span>
                                                        <span class="exif-detail" v-if="exif.ISOSpeedRatings">ISO {{exif.ISOSpeedRatings}}</span>
                                                    </v-list-item-subtitle>
                                                    <v-list-item-subtitle v-if="exif.LensModel">
                                                        {{exif.LensModel}}
                                                    </v-list-item-subtitle>
                                                </v-list-item-content>            
                                            </v-list-item>
                                            </v-card-text>
            
                                        </div>
            
                                        <div v-if="gps && gps.display_address">
                                            <v-card-text >
                                                <div class="font-weight-bold">Location</div>
                                            </v-card-text>
                                            <v-card-text v-if="gps.display_address">
                                                <div>
                                                    {{gps.display_address}} 
                                                </div>
                                            </v-card-text>
                                            <v-card-text>
                                            <vl-map :load-tiles-while-animating="true" :load-tiles-while-interacting="true"
                                                    data-projection="EPSG:4326" style="height: 300px; width:300px">
                                                <vl-view :zoom.sync="zoom" :center.sync="position" :rotation.sync="rotation"></vl-view>
            
                                                <vl-layer-tile id="osm">
                                                    <vl-source-osm></vl-source-osm>
                                                </vl-layer-tile>
                                                <vl-feature>
                                                    <vl-geom-point :coordinates="position"></vl-geom-point>
                                                    <vl-style-box>
                                                        <vl-style-icon src="/media/marker.png" :scale="0.4" :anchor="[0.5, 1]"></vl-style-icon>
                                                    </vl-style-box>
                                                </vl-feature>
                                            </vl-map>
                                            </v-card-text>
                                        </div>     
            
                                        <div>
                                            <v-card-text>
                                                <div class="font-weight-bold">
                                                    Tags
                                                    <v-combobox  
                                                        chips
                                                        multiple
                                                        deletable-chips
                                                        dense
                                                            :items="tags"
                                                            item-text="name"
                                                            item-value="id"
                                                            v-model="assetTags">
                                                            variant="underlined"
                                                        </v-combobox>
                                                </div>
                                            </v-card-text>
                                        </div>
            
                                        <div v-if="things && things.length > 0">
                                            <v-card-text>
                                                <div class="font-weight-bold">Things</div>
                                                <v-list-item>
                                                    <v-list-item-content>
                                                        <v-list-item-subtitle> 
                                                            <span v-for="(thing, index) in things" :key="index">
                                                                {{thing.label_en}}
                                                                <span v-if="index != things.length - 1">, </span>
                                                            </span>    
                                                        </v-list-item-subtitle>
                                                    </v-list-item-content>
                                                </v-list-item>
                                            </v-card-text>
                                        </div>
            
                                        <div v-if="asset.score_aesthetic || asset.score_technical">
                                            <v-card-text >
                                                <div class="font-weight-bold">Scores</div>
                                            </v-card-text>
                                            <v-list-item three-line>
                                                <v-list-item-avatar>
                                                    <v-icon>mdi-poll-box</v-icon>
                                                </v-list-item-avatar>
                                                <v-list-item-content>
                                                    <v-list-item-subtitle>Aesthetic {{asset.score_aesthetic}}</v-list-item-subtitle>
                                                    <v-list-item-subtitle>
                                                        Technical {{asset.score_technical}}
                                                    </v-list-item-subtitle>
                                                </v-list-item-content>
                                            </v-list-item>
                                        </div>
            
                                        <div v-if="photo_faces && photo_faces.length > 0">
                                            <v-card-text>
                                                <v-container>
                                                    <v-row dense no-gutters>
                                                        <v-col cols="3">
                                                            <div class="font-weight-bold">
                                                                People    
                                                            </div>
                                                        </v-col>
                                                        <v-col cols="2">
                                                            <v-switch
                                                                color="info"
                                                                v-model="asset.faces_all_identified"
                                                                label="Done">
                                                                    <v-icon color="info" >mdi-check</v-icon>
                                                            </v-switch>
                                                        </v-col>                                            
                                                    </v-row>
                                                </v-container>
                                                <v-list density="compact" dense>
                                                    <v-list-item  v-for="face in photo_faces" :key="face.id" density="compact" dense>
                                                        <v-list-item-avatar size="60">
                                                            <v-img :src="faceUrl(face.id)"></v-img>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content dense>
                                                            <span v-if="faceEditId == face.id">
                                                                <v-combobox  :search-input.sync="faceName"
                                                                    :items="knownPersons"
                                                                    item-text="name"
                                                                    item-value="id"
                                                                    v-model="newPerson">
                                                                </v-combobox>
                                                            </span> 
                                                            <span v-else>
                                                                <span v-if="face.person && face.person.confirmed">
                                                                    <v-list-item-title  
                                                                        v-html="face.person.name">
                                                                    </v-list-item-title>
                                                                    <v-list-item-subtitle class="font-italic">{{face.classified_by}} ({{face.confidence}})</v-list-item-subtitle>
                                                                    <v-list-item-subtitle class="font-italic">{{face.emotion}} ({{face.emotion_confidence}})</v-list-item-subtitle>
                                                                </span>
                                                                <v-list-item-subtitle v-else>Unknown</v-list-item-subtitle>
                                                            </span>
                                                        </v-list-item-content>
                                                        <v-list-item-action class="no-wrap flex-nowrap flex-sm-nowrap flex-row align-center" dense>
                                                            <v-btn v-if="faceEditId != face.id" icon @click="edit(face)" dense>
                                                                <v-icon>mdi-pencil</v-icon>
                                                            </v-btn>
                                                            <v-btn v-else icon @click="setPerson">
                                                                <v-icon>mdi-check</v-icon>
                                                            </v-btn>
                                                            <v-btn icon @click="reset(face)">
                                                                <v-icon>mdi-delete</v-icon>
                                                            </v-btn>
                                                            <v-btn icon @click="clickFace(face)" v-if="face.person_id">
                                                                <v-icon>mdi-image-search</v-icon>
                                                            </v-btn>
                                                        </v-list-item-action>
            
                                                    </v-list-item>
                                                </v-list>
                                            </v-card-text>
            
                                        </div>
                                    </v-card>
                                </div>
                            </v-card>
                        </v-expand-x-transition>
                    </v-col>
                </v-row>
            </v-col>
            <v-col class="noscroll ma-2" fill-height>
                <v-row fill-height>
                    <v-col class="scroll ma-2" fill-height v-if="duplicatesList">
                        Simple List of Duplicates
                        <div 
                            v-for="(assetDup, index) in duplicatesList" 
                            :index="index" 
                            :key="assetDup.path"
                            :ref="'p' + index">
                            <v-card >
                                <v-card-title>{{assetDup.path}}</v-card-title>
                                <v-card-text>
                                    <tile v-if="assetDup"
                                    :target-height="previewHeight" 
                                    @set-rating="setRating"
                                    @click-photo="clickPhoto"
                                    :asset="assetDup"
                                    >
                                    </tile> 
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <!-- <v-btn color="warning" text @click="deleteassets">Delete</v-btn> -->
                                </v-card-actions>
                            </v-card>
                        </div>  
                    </v-col>
                </v-row>
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
    import { date_utils } from "../utils/date_utils";
    import { asset_utils } from "../utils/asset_utils";

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
                gps: null,
                position: null,
                tags: null,
                things: null,
                photo_faces: null,
                exif: [],
                faceEditId: null,
                duplicatesList: null,
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
            this.loadData();
        },

        watch: {

            asset(p) {
                console.log(`called: asset ${p}`);
                if (!this.asset)
                    this.loadData(this.assetId);
            },            

        },

        computed: {
            ...mapState({
                previewHeight: state => state.person.previewHeight
                
            }),
            cssProps() {
                return {
                    '--current-tick': this.currentTick + "px",
                    '--current-tick-text': (this.currentTick - 10) + 'px',
                    '--tick-color': this.$vuetify.theme.secondary
                }
            },
            assetTags: {
                set(v) {
                    console.log(`Tag Set:`, v)
                    this.setAssetTags(v);
                },
                get() {
                    if (this.asset && this.asset.tags) {
                        return this.asset.tags.map( (tag) => tag.name );    
                    } else {
                        return [];
                    }
                }
            },
        },

         // eslint-disable-next-line no-unused-vars
        beforeRouteLeave(to, from, next) {
            next();
        },

        methods: {
            ...date_utils,
            ...asset_utils,

            loadData() {
                console.log(`called: loadData ${this.assetId}`);
                let self = this;
                axios.get(`/api/asset/data/${this.assetId}`).then((result) => {
                    self.asset = result.data;
                    console.log(`Asset loaded with id=${this.asset.id} path=${this.asset.path}`);

                    if (self.asset.gps_id) {
                        this.$store.dispatch("getGpsForPhoto", self.asset).then((gps => {
                            self.gps = gps;
                            self.position = [ gps.longitude, gps.latitude ];
                        }))
                    }
                    this.$store.dispatch("getExifForPhoto", this.asset).then((exif => {
                        self.exif = exif;
                        self.size = parseInt(exif.ExifImageWidth) * parseInt(exif.ExifImageHeight) / 1e6
                    }));
                    if (this.asset.gps_id) {
                        this.$store.dispatch("getGpsForPhoto", this.asset).then((gps => {
                            self.gps = gps;
                            self.position = [ gps.longitude, gps.latitude ];
                        }))
                    }
                    this.$store.dispatch("getThingsForPhoto", this.asset).then((things => {
                        self.things = things;
                    }));
                    this.$store.dispatch("getAllTags").then((tags => {
                        self.tags = tags;
                    }));
                    this.$store.dispatch("getAssetDuplicates", this.asset).then((duplicatesList => {
                        self.duplicatesList = duplicatesList;
                    }));
                    this.$store.dispatch("getFacesByPhoto", this.asset).then((faces => {
                        this.photo_faces = faces;
                    }));
                });
            },

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
