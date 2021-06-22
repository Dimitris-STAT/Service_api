# Ergasia2_E18151_Dimitris_Stathopoulos
  Ξεκινώντας, ένας χρήστης ενδείκνειται να ακολουθήσει κάποια συγκεκριμένα βήματα προκειμένου να ενεργοποιήσει καθώς και να χρησιμοποιήσει το web-service αυτό .Σε αρχικό στάδιο καλείται να έχει εγκατεστημένο το docker στον υπολογιστή του ,το οποίο του δίνει την δυνατότητα ενεργοποίησης και δημιουργίας τον επιμέρους images και containers των οποίων οι εντολές δημιουργίας περιέχονται στα αρχεία docker_compose και Dockerfile .Στην συνέχεια μέσω της εντολής docker-compose up --build ο χρήστης χτίζει στον υπολογιστή του τα δυο docker images docker-compose_flask-service και mongo και τα αντιστοιχά τους containers .Λόγω της χρήσης της εντολής  up το web-service αυτόματα και ύστερα απο την   επιτυχημένη εγκαταστασή του είναι έτοιμο για λειτουργία και εκτέλεση των endpoints που βρίσκονται μέσα στον κώδικα του αρχείου service_code.py .Στην συνέχεια είναι απαραίτητο να υπάρχουν στο συστημά του εφαρμογές-προγράμματα τα οποία δέχονται HTTP methods ('GET','POST','PUT', 'PATCH' και τα λοιπά) διότι ως επι το πλήστων είναι απαραίτητα για την υλοποίηση των δεδομένων endpoint .Ο λόγος που προτείνονται τέτοιου είδους προγράμματα είναι οτι οι browsers δέχονται μονο get methods .Εφόσον λοιπόν απο την μεριαά του χρήστη έχουν πραγματοποιηθεί τα προαναφερόμενα βήματα είναι πλεον στο χέρι του και την αρεσκία του χρήστη να εκτελέσει τα διάφορα endpoints.
  
   Σε δεύτερο στάδιο , θα αναλυθεί ο τρόπος λειτουργίας των endpoint που δημιουργήθηκαν καθώς και το σκεπτικό υλοποίησης .Αρχικά γίνεται λόγος για το αν ο χρήστης που θέλει να συνδεθεί στο σύστημα είναι ένας απλός χρήστης ή κανονικός διαχειριστής .Υποτίθεται οτι ένας διαχειριστής έχει την δυνατότητα να δημιουργήσει άλλους διαχειριστές μέσω του endpoint createAdmin  χωρίς όμως να γίνεται έλεγχος για το αν είναι πραγματικά ο διαχειριστής του πληροφοριακού συστήματος .Εφόσον όμως δημιουργηθεί ο διαχειριστής προκειμένου να μπορέσει να υλοποιήσει τα υπόλοιπα endpoint στα οποία υποτίθεται οτι πρέπει να έχει πρόσβαση σύμφωνα με την εκώνηση της άσκησης .Πιο αναλυτικά με την χρήση του endpoint AdminLogin  και αφού είναι επιτυχήμενη η σύνδεση  στο σύστημα δημιουργείται ένα uuid το οποίο αποτελείται μονο απο αριθμούς αλλα παρουσιάζεται σαν string και με την εισαγωγή του οποίου στην περιοχή Authorization γίνεται validation και παράλληλα δημιουργείται ενα session με ορισμένο χρονικό οριο προκειμένου να χρησιμοποιήσει τα 3 endpoint που του δίνεται η δυνατότητα να χρησιμοποιήσει .Αυτά τα endpoint είναι createProduct στο οποίο ουσιαστικά δίνει json δεδομένα για την δημιουργια ενός νεου προιόντος στο οποίο μετά την επιτυχημένη λειτουργία της μεθόδου PUT προσθέτει τα δεδομένα στο collection Products ,ένα ακόμη endpoint είναι το deleteProduct το οποίο δίνει την δυνατότητα στον διαχειριστή να διαγράψει ένα προϊον αν και εφόσον δώσει _id(ως argument) που aντιπροσωπεύει ένα ηδη υπάρχον προϊόν και τέλος ξανά με την εισαγωγή του id μπορεί ενημερώσει 4 τέσσερα απο τα πεδιά του προϊοντος .
   
   Όσον αφορά τα endpoint που αφορούν λειτουργίες του χρήστη έχουμε αρχικά ένα endpoint το οποίο επιτρέπει την δημιουργία ενός χρήστη το createUser το οποίο επιτρέπει την δημιουργία ενός χρήστη και κατά την δημιουργία αυτού προστίθεται ένα field με όνομα "category" το οποίο δηλώνει οτι είναι simple user δηλαδή απλός χρήστης .Ύστερα, ο εκάστοτε χρήστης καλείται να κάνει login καλώντας το endpoint login και κατά την επιτυχή του σύνδεση στο σύστημα παράγεται ένας κωδικός uuid ο οποίος πρέπει να δηλωθεί στην περιοχή Authorization του header .Στο επόμενο στάδιο που αφορά τις λειτουργίες του χρήστη έχουμε το endpoint getProduct το οποίο του επιτρέπει να ψάξει ένα προϊον με τρείς διαφορετικές επιλογές : name , _id ,category .Πιο συγκεκριμένα γίνεται έλεγχος για το αν ο χρήστης έχει προσθέση παραπάνω απο μία απο τις επιλογές που του δίνονται και του εμφανίζει μήνυμα οτι μόνο μία επιλογή επιτρέπεται κάθε φορα .Μετά την επιτυχημένη επιλογή του μπορεί να δεί τα προϊόντα με αλφαβητική σειρά (επιλο΄γη:name) αλλιώς μπορεί βάσει κατηγορίας των προϊόντων αυτών (επιλογή :category) και τέλος μπορεί να ψάξει ένα προϊόν με βάση το _id του .Στην συνέχεια υπάρχει η επιλογή-endpoint addToCart το οποίο του επιτρέπει να δημιουργήσει προσωρινά ενα καλάθι στο οποίο περιέχoται οι γενικότερες πληροφορίες των προϊοντων καθώς και η συνολική τιμή αυτών με βάση το απόθεμα που ζήτησε στην αρχή ως argument .Επίσης είναι απαραίτητη η δήλωση του id του προϊοντως ως header πριν το κάλεσμα του endpoint .Πιο επεξηγηματικά , δημιουργείται μια global λίστα η οποία αποθηκεύει  μέσα της τα δεδομένα του εκάστοτε προϊόντος καθώς και την συνολική τιμή των προϊόντων αυτών(η οποία τιμή υπολογίζεται στην συνάρτηση totalPRice()) .Εφόσον λοιπόν ο χρήστης έχει προσθέσει με επιτυχία τα προϊόντα της αρεσκίας του έχει την δυνατότητα να  προβάλει το καλάθι αυτο με την χρήση του endpoint viewCart το οποίο του προβάλει πληροφορίες για τον προϊόν καθώς και την τελική απόδειξη αν και εφόσον επιθυμεί να πληρώσει .Επιπρόσθετα endpoint όπς το deleteFromCart επιτρέπει στον χρήστη να διαγράψει ένα προϊόν ,η αναζήτηση του οποίου γίνεται με βάση το id του ,απο το καλάθι του και αν ε΄ίναι επιτυχής αυτή η ενέργεια του εμφανίζει τα προίόντα που έχουν απομείνει καθώς και την νέα συνολική τιμή αυτών .Ο τρόπος με τον οποίο υλοποιείται η επιστροφή του τελικού περιεχομένου του καλαθιού  είναι δημιουργία του new_total_cost το οποίο είναι public λίστα και εσωτερικά αποθηκεύεται η αφαίρεση της αρχικής τιμής hole_price της λίστας shopping_cart απο την αρχίκή συνολική τιμή .Ύστερα το total_cost παίρνει την προηγούμενη τιμή του μέιον την τιμή του hole_price και αφού ουσιαστικά μειωθεί το συνολικό κόστος διαγράφεται το προϊόν που ζητήθηκε .Στο τέλος του endpoint λιγο πρίν εμφανιστεί το αποτέλεσμα αποθηκεύουμε την νεα τελίκή τιμή των προϊόντων στην global μεταβλητή sum_cost το οποίο αργότερα θα χρησιμοποιηθεί .Ένας τρόπος χρήσης του sum_cost γίνεται απο το endpoint buyProducts το οποίο ύστερα απο την επιτυχή εισαγωγή ενός argument('card') δηλαδή την εισαγωγή ενός δεκαεξαψήφιου αριθμού ως argument ,χρησιμοποιεί το sum_cost καθώς shopping_cart για την εμφάνιση των προϊόντων και του τελικού κόστους αυτών .Ακόμη καθαρίζει το καλάθι διότι υποτίθεται οτι ο πελάτης έχει πληρώσει ήδη στο ταμείο .Στην συνέχεια υπάρχουν ακόμη endpoint που αφορούν τον χρήστη το ένα είναι το OrderHistory το οποίο κατά την κλήση του χρησιμοποιεί το email του χρήστη το οποίο χρησιμοποιήθηκε κατά την εκτέλεση του endpoint login και με την χρήση της μεθόδου update_one ενημέρωνει τα δεδομένα του χρήστη, ο οποίος βρίσκεται στο collection Users, προσθέτοντας ένα νεο field το οποίο ονομάζεται "orderHistory" και παίρνει ως str(string) τα δεδομένα που αφορούν την απόδειξή του κατα την τελευταία χρήση του endpoint buyProducts .Τέλος με την χρήστη του endpoint deleteUser ο χρήστης έχει την δυνατότητα να διαγράψει τον εαυτό του και τα δεδομένα του απο την βάση δεδομένων του πληροφοριακού συστήματος .Επίσης χρησιμοποιείται το user_email το οποίο περιέχει το email που δηλώθηκε κατα την επιτυχή σύνδεση του χρήστη στο σύστημα και ο λόγος είναι για να αποφευχθεί η διαγραφή κάποιου άλλου πελάτη απο τον εκάστοτε χρήστη.
