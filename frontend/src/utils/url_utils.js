export const url_utils = {
    generateFilterArgs(filters) {
        if (!filters) {
            return "";
        }
        let args = '?';
        for (var name in filters) {
            if (filters[name] !== null) {
                args += `&filter.${name}=${filters[name]}`
            }
        }
        return args;
    },
};