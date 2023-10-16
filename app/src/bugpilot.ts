export function bugpilotLogin(userId: number, username: string, lastLogon: string = "unknown") {
    // Set bug report options
    let url = undefined;
    if (window.location.host.includes("localhost")) {
        url =
            "https://bbb.fede.live" +
            window.location.pathname +
            window.location.search +
            window.location.hash;
    }
    window.Bugpilot.identify({
        id: userId,
        username: username,
        lastLogon: lastLogon,
        url: url,
    });
}

export function bugpilotLogout() {
    window.Bugpilot.logout();
}
