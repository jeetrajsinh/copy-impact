// Navbar layout component
// ...existing code...
 const Navbar: React.FC = () => {
   return (
     <nav className="bg-dark-card shadow-lg">
       <div className="max-w-7xl mx-auto px-4">
         <div className="flex items-center justify-between h-16">
           <div className="flex items-center">
             <FiTrendingUp className="h-8 w-8 text-brand-blue mr-2" />
             <span className="font-semibold text-xl text-gray-100">Copy Trader Analytics</span>
           </div>
           {/* Add other nav items here if needed */}
         </div>
       </div>
     </nav>
   );
 };
 export default Navbar;
