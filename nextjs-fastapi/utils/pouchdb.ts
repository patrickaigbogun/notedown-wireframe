import PouchDB from 'pouchdb'

const pdb = new PouchDB('notedown_notes')

function sync() {
    syncDom.setAttribute('data-sync-state', 'syncing');
    const opts = {live: true};
    db.replicate.to(remoteCouch, opts, syncError);
    db.replicate.from(remoteCouch, opts, syncError);
  }