import React, { useState, useEffect } from 'react';

interface SidebarProps {
   onFetchData: (mainWallet: string, masterWallets: string[]) => void;
   isFetching: boolean;
 }

 const Sidebar: React.FC<SidebarProps> = ({ onFetchData, isFetching }) => {
   const [mainWallet, setMainWallet] = useState('');
   const [masterWalletsStr, setMasterWalletsStr] = useState('');

   // Load saved wallets from localStorage on mount
   useEffect(() => {
     const savedMain = localStorage.getItem('mainWallet');
     const savedMasters = localStorage.getItem('masterWalletsStr');
     if (savedMain) setMainWallet(savedMain);
     if (savedMasters) setMasterWalletsStr(savedMasters);
   }, []);

   const handleSaveConfig = () => {
     localStorage.setItem('mainWallet', mainWallet);
     localStorage.setItem('masterWalletsStr', masterWalletsStr);
     alert('Configuration saved locally!'); // Simple feedback
   };
   
   const handleSubmit = () => {
     const masterWalletsArray = masterWalletsStr.split('\n').map(w => w.trim()).filter(w => w);
     onFetchData(mainWallet.trim(), masterWalletsArray);
   };

   return (
     <aside className="w-72 bg-dark-card p-6 space-y-6 h-full fixed top-16 left-0 overflow-y-auto shadow-lg"> {/* Adjust top-16 if navbar height changes */}
       <div>
         <label className="block text-gray-400 mb-2 font-semibold">Main Wallet Address</label>
         <input
           type="text"
           className="w-full p-2 rounded bg-dark-bg text-gray-100 border border-gray-700 focus:outline-none focus:border-brand-blue"
           value={mainWallet}
           onChange={e => setMainWallet(e.target.value)}
           placeholder="Enter main wallet address"
         />
       </div>
       <div>
         <label className="block text-gray-400 mb-2 font-semibold">Master Wallet Addresses (one per line)</label>
         <textarea
           className="w-full p-2 rounded bg-dark-bg text-gray-100 border border-gray-700 focus:outline-none focus:border-brand-blue"
           rows={6}
           value={masterWalletsStr}
           onChange={e => setMasterWalletsStr(e.target.value)}
           placeholder="Enter master wallet addresses, one per line"
         />
       </div>
       <div className="flex space-x-2">
         <button
           className="bg-brand-blue text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
           onClick={handleSubmit}
           disabled={isFetching}
         >
           {isFetching ? 'Fetching...' : 'Analyze'}
         </button>
         <button
           className="bg-gray-700 text-gray-200 px-4 py-2 rounded hover:bg-gray-600"
           onClick={handleSaveConfig}
         >
           Save Config
         </button>
       </div>
     </aside>
   );
 };
 export default Sidebar;