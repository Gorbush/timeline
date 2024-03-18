export const asset_utils = {
    isPhoto(asset) {
        return asset.asset_type == 'jpg' || asset.asset_type == 'heic';
    },
    videoSource(asset) {
        return this.isPhoto(asset) ? null : encodeURI(this.$basePath + "/assets/video/full/" + asset.path + ".mp4");
    },
    photoUrl(asset) {
        if (asset)
            if (asset.asset_type == "mp4" || asset.asset_type == "mov")
                return encodeURI(this.$basePath + "/assets/video/full/" + asset.path + ".mp4");
            else
                return encodeURI(this.$basePath + "/assets/full/" + asset.path);
    },

    faceUrl(id) {
        return this.$basePath + "/api/face/preview/80/" + id + ".png";
    },
    assetUrl(asset) {
        return encodeURI("/#/asset?asset_id=" + asset.id)
    },
    wallUrl(asset) {
        return encodeURI("/#/wall?asset_id=" + asset.id)
    },

}