from playwright.sync_api import sync_playwright

def extract_ra_result(page):
    page.evaluate("""
    () => {
      document
        .querySelectorAll('#accordion .panel-collapse')
        .forEach(p => p.classList.add('in'));
    }
    """)

    ra_data = page.evaluate(r"""
    () => {
        const getText = (label, el) => {
            return Array.from(el.querySelectorAll('p'))
            .find(p => p.querySelector('strong')?.innerText.includes(label))
            ?.querySelector('span')
            ?.innerText.trim() || null;
        };
        const ra_No = document.querySelector('.block_bid_no b')?.innerText || null;

/* ================= RA DETAILS ================= */
        const raDetailsOuterPanel = Array.from(
            document.querySelectorAll('.panel.panel-default')
          ).find(panel =>
            panel.querySelector('.panel-heading a')
              ?.innerText?.includes('RA DETAILS')
          );

        const raDetailsOuterPanel = raDetailsOuterPanel?.querySelector('.panel-body') || null;
                  
        /* ---------- RA DETAILS ---------- */
        const raDetailsOuterPanel  = Array.from(
            raDetailsOuterPanel .querySelectorAll('.border.block')
              ).find(b => b.innerText.includes('Bid Number:'));
          
        let raInfo = {};
                            
        if (raDetailPanelBody) {
            const raDetailsBlock = Array.from(
            raDetailPanelBody.querySelectorAll('.border.block')
            .find(b=> b.innerText.includes('Bid Number'));
                            
          if (raDetailsBlock) {
            raInfo = {
                            
            raStatus : getText('RA Status:', raDetailsBlock),
            raQuantity : getText('Quantity:', raDetailsBlock),
            raLifeCycyle : getText('RA Life Cycle', raDetailsBlock),
            raValidity : getText('RA Validity', raDetailsBlock),
       
            raStartDate : getText('RA Start Date / Time:', raDetailsBlock),
            raEndDate : getText('RA End Date / Time:', raDetailsBlock)
            
            raAverageTurnOver = Array.from(document.querySelectorAll('.col-block strong'))
                     .find(s => s.innerText.includes('Average Turn Over'))
                     ?.parentElement.querySelector('span')
                     ?.innerText.trim() || null,
            raGovExpRequired = Array.from(document.querySelectorAll('.col-block strong'))
                                 .find(s => s.innerText.includes('Experience with Gov.'))
                                 ?.parentElement.querySelector('span')
                                 ?.innerText.trim() || null
            };
          }
        }
        
        /* ---------- BUYER DETAILS ---------- */
        const raBuyerBlock = Array.from(
            ra_DetailPanelBody.querySelectorAll('.border.block')
            ).find(b => b.innerText.includes('Buyer Details'));
        
        let raBuyerDetails = {};
        if (ra_buyerBlock) {
            raBuyerDetails.name = getText('Name', ra_buyerBlock);
            raBuyerDetails.address = getText('Address:', ra_buyerBlock);
            raBuyerDetails.ministry = getText('Ministry', ra_buyerBlock);
            raBuyerDetails.department = getText('Department', ra_buyerBlock);
            raBuyerDetails.organisation = getText('Organisation', ra_buyerBlock);
            raBuyerDetails.office = getText('Office', ra_buyerBlock);
            }

/* ================= TECHNICAL EVALUATION ================= */ 
        const getColumnIndexMap = (table) => {
            const headerMap = {};

            table.querySelectorAll('thead th').forEach((th, i) =>{
              headerMap[th.innerText.replace(/\s+/g, ' ').trim().toLowerCase()] = i;
              });
              return headerMap;
        };

        const raTechnicalEvaluationPanel = Array.from(
                document.querySelectorAll('.panel.panel-default')
                ).find(panel =>
                panel.querySelector('.panel-heading a')
                ?.innerText?.includes('TECHNICAL EVALUATION')
                );

        const raTechnicalEvaluationPanelBody = raTechnicalEvaluationPanel?.querySelector('.panel-body');
        const raTechnicalEvaluationTable = raTechnicalEvaluationPanelBody?.querySelector('table');
        const raTechnicalEvaluationTableBody = raTechnicalEvaluationTable?.querySelector('tbody');
        
        let technicalEvaluation = [];

      if (raTechTable && raTechTbody) {
        const colIndex = getColumnIndexMap(raTechTable);

        const getCell = (row, header) => {
          const idx = colIndex[header.toLowerCase()];
          return idx !== undefined ? row.querySelectorAll('td')[idx] : null;
        };

        technicalEvaluation = Array.from(raTechTbody.querySelectorAll('tr')).map(row => ({
          serialNo: getCell(row, 's.no.')?.innerText.trim() || null,
          sellerName: getCell(row, 'seller name')?.innerText.trim() || null,
          offeredItem: getCell(row, 'offered item')?.innerText.trim() || null,
          offerSubmittedOn: getCell(row, 'offer submitted on')?.innerText.trim() || null,
          qualificationStatus: getCell(row, 'status')?.innerText.trim() || null,

          mseMiiLabels : getCell(row, 'mse/mii status')
                    ? Array.from(
                        getCell(row, 'mse/mii status').querySelectorAll('.label')
                        ).map(l => l.innerText.trim())
                    : [],

          mseMiiInfo : getCell(row, 'mse/mii status')
                    ? Array.from(
                        getCell(row, 'mse/mii status').querySelectorAll('i.fa-info-circle')
                        )
                        .map(i => i.title?.trim())
                        .filter(Boolean)
                    : []
        }));
      }



/* ================= RA FINANCIAL EVALUATION ================= */

const raFinancialEvaluationPanel = Array.from(
  document.querySelectorAll('.panel.panel-default')
).find(panel =>
  panel.querySelector('.panel-heading a')
    ?.innerText
    ?.includes('FINANCIAL EVALUATION')
);

let raWinnerList = [];
let financialEvaluationAvailable = true;

if (!raFinancialEvaluationPanel) {
  financialEvaluationAvailable = false;
} else {
  const raFinancialEvaluationPanelBody =
    raFinancialEvaluationPanel.querySelector('.panel-body');

  const raFinancialEvaluationTable =
    raFinancialEvaluationPanelBody?.querySelector('table');

  const raFinancialEvaluationTableBody =
    raFinancialEvaluationTable?.querySelector('tbody');

  if (raFinancialEvaluationTable && raFinancialEvaluationTableBody) {
    const rows = raFinancialEvaluationTableBody.querySelectorAll('tr');

    if (rows.length > 0) {
      const colIndex = getColumnIndexMap(raFinancialEvaluationTable);

      const getCell = (row, headerName) => {
        const idx = colIndex[headerName.toLowerCase()];
        return idx !== undefined ? row.querySelectorAll('td')[idx] : null;
      };

      raWinnerList = Array.from(rows).map(row => {
        const rankCell = getCell(row, 'rank');

        return {
          serialNo:
            getCell(row, 's.no.')?.innerText.trim() || null,

          sellerName:
            getCell(row, 'seller name')?.innerText.trim() || null,

          offeredItem:
            getCell(row, 'offered item')
              ?.innerText.replace(/\s+/g, ' ')
              .trim() || null,

          offerSubmittedOn:
            getCell(row, 'offer submitted on')?.innerText.trim() || null,

          mseMiiLabels:
            getCell(row, 'mse/mii status')
              ? Array.from(
                  getCell(row, 'mse/mii status').querySelectorAll('.label')
                ).map(l => l.innerText.trim())
              : [],

          mseMiiInfo:
            getCell(row, 'mse/mii status')
              ? Array.from(
                  getCell(row, 'mse/mii status').querySelectorAll('i.fa-info-circle')
                )
                  .map(i => i.title?.trim())
                  .filter(Boolean)
              : [],

          totalPrice:
            getCell(row, 'total price')?.innerText.trim() || null,

          rank:
            rankCell?.innerText.trim() || null,

          isWinner:
            rankCell?.querySelector('i.fa.fa-trophy')
              ? 'Winner'
              : 'NA',

          qualificationStatus:
            getCell(row, 'status')?.innerText.trim() || null
        };
      });
    }
  }
        
      return {
        ra_No,
        technicalEvaluation : raSellersList,
        financialEvaluation : {
          available : financialEvaluationAvailable,
          results : raWinnerList
        }
      };
    }
    """)
    return ra_data


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    )
    page = context.new_page()
    page.goto(
            # "https://bidplus.gem.gov.in/all-bids",
            "https://bidplus.gem.gov.in/bidding/bid/getBidResultView/1213379",
            wait_until="domcontentloaded"
        )

    page.wait_for_function("() => typeof bidStatusTypeFilter === 'function'")

    page.evaluate("""
    () => {
      bidStatusTypeFilter('bidrastatus');
    }
    """)

    page.wait_for_function("""
    () => {
      const el = document.getElementById('ra_completed');
      return el && !el.disabled && el.offsetParent !== null;
    }
    """, timeout=10000)

    page.evaluate("""
            () => {
              bidStatusFilter('ra_completed');
            }
            """)

    page.wait_for_function("""
    () => {
      const cards = document.querySelectorAll('#bidCard .card');
      if (!cards.length) return false;

      return Array.from(cards).every(card => {
        const status = card.querySelector('.text-success, .text-info')?.innerText || '';
        return /RA\\s+(Completed|Awarded)/i.test(status);
      });
    }
    """, timeout=30000)

    cards = page.evaluate("""
    () => {
      const cards = Array.from(document.querySelectorAll('#bidCard .card'));

      return cards.map(card => {
      
         /* ---------- HEADER ---------- */
        const bidAnchor = card.querySelector('.bid_no_hover[href*="showbidDocument"]');
        const raAnchor = card.querySelector(
          '.bid_no_hover[href*="showradocument"], .bid_no_hover[href*="list-ra-schedules"]'
        );
        const status = card.querySelector('.text-success')?.innerText.trim() || null;
        
         // ---------- BODY ---------- //
        const cardBody = card.querySelector('.card-body');
        const bodyRow = cardBody.querySelector('.row')
        
        // ---------- ITEMS ---------- //
        let items = null;

        const itemsRow = Array.from(bodyRow.querySelectorAll('.row'))
          .find(r => r.querySelector('strong')?.innerText.includes('Items'));

        if (itemsRow) {
          const popover = itemsRow.querySelector('a[data-toggle="popover"]');
          items = popover
            ? popover.getAttribute('data-content')?.trim()
            : itemsRow.innerText.replace('Items:', '').trim();
        }
        
        // ---------- QUANTITY ---------- //
        let quantity = null;
        const qtyRow = Array.from(card.querySelectorAll('.row'))
          .find(r => r.querySelector('strong')?.innerText.includes('Quantity'));

        if (qtyRow) {
          quantity = qtyRow.innerText.replace('Quantity:', '').trim();
        }

        // ---------- DEPARTMENT ---------- //
        let ministry = null;
        let department = null;

        const deptBlock = card.querySelector('.col-md-5');
        if (deptBlock) {
          const lines = deptBlock.innerText
            .split('\\n')
            .map(t => t.trim())
            .filter(t => t && !t.includes('Department Name And Address'));

          ministry = lines[0] || null;
          department = lines.slice(1).join(', ') || null;
        }
        
        // ---------- RESULTS ---------- //
        
        const links = card?.querySelectorAll('a[href*="/bidding/bid/getBidResultView/"]') || [];
                        
        let bidResultURL = null;
        let raResultURL = null;
        
        links.forEach(link => {
          const button = link.querySelector('.btn.btn-primary');
        
          if (!button) return;

          if (button.value === 'View Bid Results' ||  button.value === 'View BID Results') {
            bidResultURL = link.href;
          } else if (button.value === 'View RA Results') {
            raResultURL = link.href;
          }
        });

        return {
          status,
          ra_No: bidAnchor?.textContent.trim() || null,
          bidURL: bidAnchor?.href || null,
          raNo: raAnchor?.textContent.trim() || null,
          raURL: raAnchor?.href || null,
          items,
          quantity,
          ministry,
          department,
          bidResultURL,
          raResultURL,
          start_date: card.querySelector('.start_date')?.innerText.trim() || null,
          end_date: card.querySelector('.end_date')?.innerText.trim() || null
        };
      });
    }
    """)
      
    for card in cards[:1]:
        print(card)
        raResultURL = card.get("raResultURL")
        if not raResultURL:
            continue
        
        print("Opening RA Result: ", raResultURL())
        raResultPage = context.new_page()
        try:
            raResultPage.goto(raResultURL, wait_until = "domcontentloaded")
            raResultPage.wait_for_selector('#content', timeout = 15000)

            raResultData = extract_ra_result(raResultPage)
            print(raResultData)
            
            card['raResult'] = raResultData
            print(cards)
        finally:
            raResultPage.close()

    page.close()
