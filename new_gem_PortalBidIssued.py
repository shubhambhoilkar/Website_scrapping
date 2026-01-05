from playwright.sync_api import sync_playwright

def extract_ra_result(page):
    page.evaluate("""
    () => {
      document
        .querySelectorAll('#accordion .panel-collapse')
        .forEach(p => p.classList.add('in'));
    }
    """)

    bid_data = page.evaluate(r"""
    () => {
        const getText = (label, el) => {
            return Array.from(el.querySelectorAll('p'))
            .find(p => p.querySelector('strong')?.innerText.includes(label))
            ?.querySelector('span')
            ?.innerText.trim() || null;
        };
        const ra_No = document.querySelector('.block_bid_no b')?.innerText || null;

/* ================= RA DETAILS ================= */
        const ra_DetailsPanel = Array.from(
            document.querySelectorAll('.panel.panel-default')
            ).find(panel =>
            panel.querySelector('.panel-heading a')
            ?.innerText
            ?.includes('BID DETAILS')
            );

        const ra_DetailPanelBody = ra_DetailsPanel?.querySelector('.panel-body') || null;
                  
        /* ---------- RA DETAILS ---------- */
        const ra_DetailsPanel = Array.from(
            ra_DetailPanelBody.querySelectorAll('.border.block')
              ).find(b => b.innerText.includes('Bid Number:'));
          
        let raInfo = {};
        if (ra_DetailsPanel) {
            raInfo.raStatus = getText('RA Status:', ra_DetailsPanel);
            raInfo.raQuantity = getText('Quantity:', ra_DetailsPanel);
            raInfo.raLifeCycyle = getText('RA Life Cycle', ra_DetailsPanel);
            raInfo.raValidity = getText('RA Validity', ra_DetailsPanel);
            
            raInfo.raStartDate = getText('RA Start Date / Time:', ra_DetailsPanel);
            raInfo.raEndDate = getText('RA End Date / Time:', ra_DetailsPanel);
            
            raInfo.raAverageTurnOver = Array.from(document.querySelectorAll('.col-block strong'))
                                  .find(s => s.innerText.includes('Average Turn Over'))
                                  ?.parentElement.querySelector('span')
                                  ?.innerText.trim() || null;
            raInfo.raGovExpRequired = Array.from(document.querySelectorAll('.col-block strong'))
                                 .find(s => s.innerText.includes('Experience with Gov.'))
                                 ?.parentElement.querySelector('span')
                                 ?.innerText.trim() || null;
            }
        
        /* ---------- BUYER DETAILS ---------- */
        const raBuyerBlock = Array.from(
            bidDetailPanelBody.querySelectorAll('.border.block')
            ).find(b => b.innerText.includes('Buyer Details'));
        
        let ra_buyerDetails = {};
        if (ra_buyerBlock) {
            ra_buyerDetails.name = getText('Name', ra_buyerBlock);
            ra_buyerDetails.address = getText('Address:', ra_buyerBlock);
            ra_buyerDetails.ministry = getText('Ministry', ra_buyerBlock);
            ra_buyerDetails.department = getText('Department', ra_buyerBlock);
            ra_buyerDetails.organisation = getText('Organisation', ra_buyerBlock);
            ra_buyerDetails.office = getText('Office', ra_buyerBlock);
            }

/* ================= TECHNICAL EVALUATION ================= */ 
        const getColumnIndexMap = (table) => {
            const headerMap = {};
            const headers = table.querySelectorAll('thead th');
            
            headers.forEach((th, index) => {
            const key = th.innerText.replace(/\s+/g, ' ').trim().toLowerCase();
            headerMap[key] = index;
            });
            
            return headerMap;
        };

        const raTechnicalEvaluationPanel = Array.from(
                document.querySelectorAll('.panel.panel-default')
                ).find(panel =>
                panel.querySelector('.panel-heading a')
                ?.innerText
                ?.includes('TECHNICAL EVALUATION')
                );

        const raTechnicalEvaluationPanelBody = raTechnicalEvaluationPanel.querySelector('.panel-body')
        const raTechnicalEvaluationTable = raTechnicalEvaluationPanelBody.querySelector('table');
        const raTechnicalEvaluationTableBody = raTechnicalEvaluationTable?.querySelector('tbody');
        
        let raSellersList = [];

        if (raTechnicalEvaluationTable && raTechnicalEvaluationTableBody) {
            const colIndex = getColumnIndexMap(raTechnicalEvaluationTable);
                             
            const getCell = (headerName) => {
                    const idx = colIndex[headerName.toLowerCase()];
                    return idx !== undefined ? cells[idx] : null;
                };
            
              raSellersList = Array.from(raTechnicalEvaluationTableBody.querySelectorAll('tr')).map(row => 
                {
                return {
                serialNo:
                    getCell(row, 's.no.')?.innerText.trim() || null,

                sellerName:
                    getCell(row, 'seller name')?.innerText.trim() || null,

                offeredItem:
                    getCell(row, 'offered item')?.innerText.replace(/\s+/g, ' ').trim() || null,

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

                qualificationStatus:
                    getCell(row, 'status')?.innerText.trim() || null
                };
            });
        }


/* ================= FINANCIAL EVALUATION ================= */ 
        const financialEvaluationPanel = Array.from(
            document.querySelectorAll('.panel.panel-default')
            ).find(panel =>
            panel.querySelector('.panel-heading a')
            ?.innerText
            ?.includes('FINANCIAL EVALUATION')
            );    
        
        const financialEvaluationPanelBody =
          financialEvaluationPanel.querySelector('.panel-body');
        
        const financialEvaluationPanelTable = financialEvaluationPanelBody?.querySelector('table');
        const financialEvaluationPanelTableBody = financialEvaluationPanelTable?.querySelector('tbody');
        
        let winnerList = [];
        
        if (financialEvaluationPanelTable && financialEvaluationPanelTableBody) {
          const colIndex = getColumnIndexMap(financialEvaluationPanelTable);
        
          winnerList = Array.from(financialEvaluationPanelTableBody.querySelectorAll('tr')).map(row => {
            const cells = row.querySelectorAll('td');
        
            const getCell = (headerName) => {
              const idx = colIndex[headerName.toLowerCase()];
              return idx !== undefined ? cells[idx] : null;
            };
        
            return {
              serialNo:
                row.querySelector('.productDtl')?.innerText.trim() || null,
        
              sellerName:
                getCell('seller name')?.innerText.trim() || null,
        
              offeredItem:
                getCell('offered item')?.innerText.trim() || null,
              
              offerSubmittedOn:
                getCell('Offer submitted')?.innerText.trim() || null;
                             
              MSE/MII Status:
                getCell('')?.innerText.trim() || null;
        
              totalPrice:
                getCell('total price')?.innerText.trim() || null,
              
              rank: getCell('rank')?.innerText.trim()||null,
              
              isWinner:
                getCell('rank')?.querySelector('i.fa.fa-trophy')
                  ? 'Winner'
                  : 'NA',
        
              qualificationStatus:
                getCell('status')?.innerText.trim() || null
            };
          });
        }
        
      return {
        ra_No,
        'technicalEvaluation':raSellersList,
        'financialEvaluation': winnerList
        
     
      };
    }
    """)
    return bid_data


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
            "https://bidplus.gem.gov.in/all-bids",
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
      const el = document.getElementById('bid_awarded');
      return el && !el.disabled && el.offsetParent !== null;
    }
    """, timeout=10000)

    page.evaluate("""
            () => {
              bidStatusFilter('bid_awarded');
            }
            """)

    page.wait_for_function("""
    () => {
      const cards = document.querySelectorAll('#bidCard .card');
      if (!cards.length) return false;

      return Array.from(cards).every(card => {
        const status = card.querySelector('.text-success')?.innerText || '';
        return status.includes('Bid Award');
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
        bidResultURL = card.get("bidResultURL")
        raResultURL = card.get("raResultURL")
        if bidResultURL:
            print(bidResultURL)
            bidResultPage = context.new_page()
            bidResultPage.goto(bidResultURL, wait_until="domcontentloaded")
            bidResultPage.wait_for_selector('#content')
            bidResultData = extract_ra_result(bidResultPage)
            print(bidResultData)
            card['bidResult'] = bidResultData
            print(cards)
    page.close()
  
