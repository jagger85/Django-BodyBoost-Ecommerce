// Toast icons and colors configuration
const toastConfig = {
    info: {
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="stroke-info"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>`,
    },
    warning: {
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="stroke-warning"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>`,
    },
    error: {
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="stroke-error"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>`,
    },
    success: {
        icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="stroke-success"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>`,
    }
};

document.addEventListener('DOMContentLoaded', function() {
    const toastContainer = document.querySelector(".toast");
    const toastBody = document.getElementById("toast-body");
    const toastIcon = document.getElementById("toast-icon");

    htmx.on("showMessage", (e) => {
        console.log('Show message event received:', e);
        if (toastBody && toastContainer && toastIcon) {
            const type = e.detail.type;
            const config = toastConfig[type] || toastConfig.info;
            
            // Set icon and message
            toastIcon.innerHTML = config.icon;
            toastBody.textContent = e.detail.message;

            // Show toast
            toastContainer.classList.remove('hidden');
            
            // Hide after 3 seconds
            setTimeout(() => {
                toastContainer.classList.add('hidden');
            }, 3000);
        } else {
            console.error('Toast elements not found');
        }
    });
});



// response = render(request, 'store/partials/variant_control/variant_actions.html', context)
    
// # Create the toast message trigger along with the cartUpdate trigger
// triggers = {
//     'cartUpdate': True,
//     'showMessage': {
//         'message': f'{variant.product.name} added to cart!',
//         'type': 'success'
//     }
// }
// response['HX-Trigger'] = json.dumps(triggers)
// return response