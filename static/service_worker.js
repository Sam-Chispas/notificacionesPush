self.addEventListener("push", function(event) {
    let data = { title: "Notificación", body: "Tienes un nuevo mensaje" };

    if (event.data) {
        data = event.data.json();
    }

    event.waitUntil(
        self.registration.showNotification(data.title, {
            body: data.body,
            icon: "icon.png"  // Opcional: no es necesario un ICON, no es critico-
        })
    );
});
