export const url_utils = {
    generateFilterArgs(filters) {
        if (!filters) {
            return "";
        }
        let args = '?';
        for (var name in filters) {
            args += `&filter.${name}=${filters[name]}`
        }
        return args;
    },
};