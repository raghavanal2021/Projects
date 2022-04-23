export const LOAD_STATUS = "updateload"


export function updateloadstatus(msg) {
    return {
        type: LOAD_STATUS,
        payload:msg
    }
}