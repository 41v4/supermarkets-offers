// used for expired offers modal window
const app = () => {
    let showModal = false;
    let currentOffer = {};
    return {
        showModal,
        currentOffer,
        toggleModal() {
            this.showModal = !this.showModal;
        }
    }
}