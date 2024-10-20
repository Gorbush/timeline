import moment from "moment"

export const date_utils = {
    date(d) {
        return moment(d).format("DD.MM.YYYY");
    },

    time(d) {
        return moment(d).format("dddd, H:mm");
    },

}