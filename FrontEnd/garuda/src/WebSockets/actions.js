export const LOAD_STATUS = "updateload"
export const SCREENER = "screener"

export function updateloadstatus(msg) {
    return {
        type: LOAD_STATUS,
        payload:msg
    }
}

export function updatescreener(msg) {
    return {
        type: SCREENER,
        payload:msg
    }
}