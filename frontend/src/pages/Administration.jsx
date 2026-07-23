import { useEffect, useState } from "react";
import api from "../api/client";
import { formaterMontant, formaterDate, classeStatut } from "../utils/format";

export default function Administration() {
  const [resume, setResume] = useState(null);
  const [paiements, setPaiements] = useState([]);
  const [impots, setImpots] = useState([]);
  const [chargement, setChargement] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/impots/resume/"),
      api.get("/paiements/"),
      api.get("/impots/"),
    ])
      .then(([r, p, i]) => {
        setResume(r.data);
        setPaiements(p.data.results);
        setImpots(i.data.results);
      })
      .finally(() => setChargement(false));
  }, []);

  if (chargement) return <p className="chargement">Chargement…</p>;

  return (
    <div>
      <div className="entete-page">
        <div>
          <h1>Administration</h1>
          <p className="sous-titre">Suivi global des impôts et des paiements.</p>
        </div>
      </div>

      <div className="grille-cartes">
        <div className="carte-stat">
          <span className="stat-libelle">Impôts enregistrés</span>
          <span className="stat-valeur">{resume.nombre_impots}</span>
        </div>
        <div className="carte-stat">
          <span className="stat-libelle">Montant recouvré</span>
          <span className="stat-valeur vert">{formaterMontant(resume.total_paye)}</span>
        </div>
        <div className="carte-stat">
          <span className="stat-libelle">Reste à recouvrer</span>
          <span className="stat-valeur">{formaterMontant(resume.total_du)}</span>
        </div>
        <div className="carte-stat">
          <span className="stat-libelle">En retard</span>
          <span className="stat-valeur rouge">{resume.nombre_en_retard}</span>
        </div>
      </div>

      <div className="section">
        <div className="section-entete">
          <h2>Derniers paiements</h2>
        </div>
        {paiements.length === 0 ? (
          <div className="vide">Aucun paiement enregistré.</div>
        ) : (
          <div className="tableau-conteneur">
            <table className="tableau">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Contribuable</th>
                  <th>Impôt</th>
                  <th>Moyen</th>
                  <th>Montant</th>
                  <th>Statut</th>
                </tr>
              </thead>
              <tbody>
                {paiements.slice(0, 15).map((p) => (
                  <tr key={p.id}>
                    <td>{formaterDate(p.date_creation)}</td>
                    <td className="mono">{p.reference_transaction}</td>
                    <td>{p.impot_libelle}</td>
                    <td>{p.moyen_libelle}</td>
                    <td>{formaterMontant(p.montant)}</td>
                    <td>
                      <span className={classeStatut[p.statut]}>{p.statut_libelle}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="section">
        <div className="section-entete">
          <h2>Impôts par contribuable</h2>
          <a className="btn btn-secondaire btn-sm" href={`${import.meta.env.VITE_API_URL || "http://localhost:8000"}/admin/`} target="_blank" rel="noreferrer">
            Console Django
          </a>
        </div>
        <div className="tableau-conteneur">
          <table className="tableau">
            <thead>
              <tr>
                <th>Contribuable</th>
                <th>Libellé</th>
                <th>Montant</th>
                <th>Échéance</th>
                <th>Statut</th>
              </tr>
            </thead>
            <tbody>
              {impots.slice(0, 20).map((i) => (
                <tr key={i.id}>
                  <td>{i.contribuable}</td>
                  <td>{i.libelle}</td>
                  <td>{formaterMontant(i.montant)}</td>
                  <td>{formaterDate(i.date_echeance)}</td>
                  <td>
                    <span className={classeStatut[i.statut_courant]}>{i.statut_libelle}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
